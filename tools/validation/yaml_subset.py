"""Dependency-free parser for the YAML subset used by repository metadata."""

import ast
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class YamlError(ValueError):
    """A deterministic YAML parsing failure."""

    line: int
    detail: str

    def __str__(self) -> str:
        return "line {}: {}".format(self.line, self.detail)


def _scalar(value: str, line: int) -> Any:
    value = value.strip()
    if not value:
        return None
    if value in ("null", "Null", "NULL", "~"):
        return None
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith(("'", '"')):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            raise YamlError(line, "invalid quoted scalar")
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
        return int(value)
    return value


def parse_yaml(text: str) -> Any:
    """Parse mappings, sequences, and scalars used by this repository."""

    tokens = []  # type: List[Tuple[int, str, int]]
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line[: len(raw_line) - len(raw_line.lstrip())]:
            raise YamlError(line_number, "tabs are not valid indentation")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        tokens.append((indent, raw_line.strip(), line_number))

    if not tokens:
        return {}

    def parse_block(index: int, indent: int):
        is_sequence = tokens[index][1].startswith("- ")
        container = [] if is_sequence else {}

        while index < len(tokens):
            current_indent, content, line = tokens[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise YamlError(line, "unexpected indentation")

            if is_sequence:
                if not content.startswith("- "):
                    break
                item = content[2:].strip()
                if not item:
                    if index + 1 >= len(tokens) or tokens[index + 1][0] <= indent:
                        raise YamlError(line, "sequence item has no value")
                    value, index = parse_block(index + 1, tokens[index + 1][0])
                    container.append(value)
                    continue
                if ":" in item and not item.startswith(("'", '"')):
                    key, raw_value = item.split(":", 1)
                    mapping = {key.strip(): _scalar(raw_value, line)}
                    index += 1
                    while index < len(tokens) and tokens[index][0] > indent:
                        nested_indent, nested_content, nested_line = tokens[index]
                        if nested_content.startswith("- ") or ":" not in nested_content:
                            raise YamlError(nested_line, "invalid sequence mapping")
                        nested_key, nested_value = nested_content.split(":", 1)
                        nested_key = nested_key.strip()
                        if nested_key in mapping:
                            raise YamlError(nested_line, "duplicate key '{}'".format(nested_key))
                        if nested_value.strip():
                            mapping[nested_key] = _scalar(nested_value, nested_line)
                            index += 1
                        else:
                            if index + 1 >= len(tokens) or tokens[index + 1][0] <= nested_indent:
                                mapping[nested_key] = None
                                index += 1
                            else:
                                mapping[nested_key], index = parse_block(
                                    index + 1, tokens[index + 1][0]
                                )
                    container.append(mapping)
                    continue
                container.append(_scalar(item, line))
                index += 1
                continue

            if content.startswith("- ") or ":" not in content:
                raise YamlError(line, "expected a key-value mapping")
            key, raw_value = content.split(":", 1)
            key = key.strip()
            if not key:
                raise YamlError(line, "mapping key is empty")
            if key in container:
                raise YamlError(line, "duplicate key '{}'".format(key))
            if raw_value.strip():
                container[key] = _scalar(raw_value, line)
                index += 1
            elif index + 1 < len(tokens) and tokens[index + 1][0] > indent:
                container[key], index = parse_block(index + 1, tokens[index + 1][0])
            else:
                container[key] = None
                index += 1
        return container, index

    parsed, final_index = parse_block(0, tokens[0][0])
    if final_index != len(tokens):
        raise YamlError(tokens[final_index][2], "could not parse document")
    return parsed


def extract_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Return parsed YAML front matter and the Markdown body."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise YamlError(1, "opening frontmatter delimiter is missing")
    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        raise YamlError(len(lines) or 1, "closing frontmatter delimiter is missing")
    parsed = parse_yaml("\n".join(lines[1:closing]))
    if not isinstance(parsed, dict):
        raise YamlError(2, "frontmatter must be a mapping")
    return parsed, "\n".join(lines[closing + 1 :])
