"""Security tests for repository-contained tool input and evidence paths."""

import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from tests.test_context_index_selection import ContextFixture
from tools.context.cli import main as context_main
from tools.repository_paths import contained_repository_path
from tools.validation.cli import main as validation_main


class RepositoryPathTests(unittest.TestCase):
    def setUp(self):
        self.repository = tempfile.TemporaryDirectory()
        self.outside = tempfile.TemporaryDirectory()
        self.root = Path(self.repository.name)
        self.outside_root = Path(self.outside.name)

    def tearDown(self):
        self.outside.cleanup()
        self.repository.cleanup()

    def test_repository_relative_and_nested_paths_are_preserved(self):
        self.assertEqual(
            self.root.resolve() / "evidence.json",
            contained_repository_path(self.root, "evidence.json"),
        )
        self.assertEqual(
            self.root.resolve() / "reports" / "nested" / "evidence.json",
            contained_repository_path(self.root, "reports/nested/evidence.json"),
        )

    def test_absolute_outside_and_parent_traversal_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            contained_repository_path(self.root, self.outside_root / "evidence.json")
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            contained_repository_path(self.root, "../evidence.json")

    def test_symlink_escape_is_rejected(self):
        link = self.root / "escaped"
        try:
            link.symlink_to(self.outside_root, target_is_directory=True)
        except OSError as error:
            self.skipTest("symlinks are unavailable: {}".format(error))
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            contained_repository_path(self.root, "escaped/evidence.json")


class ContextCliPathTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ContextFixture()
        self.outside = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.outside.cleanup()
        self.fixture.close()

    def run_cli(self, arguments):
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()) as errors:
            result = context_main(("--root", str(self.fixture.root)) + tuple(arguments))
        return result, errors.getvalue()

    def test_index_accepts_nested_repository_output(self):
        result, _ = self.run_cli(("index", "--output", ".context-reports/nested/index.json"))
        self.assertEqual(0, result)
        self.assertTrue(
            (self.fixture.root / ".context-reports" / "nested" / "index.json").is_file()
        )

    def test_index_rejects_absolute_outside_output_and_parent_traversal(self):
        for unsafe in (str(Path(self.outside.name) / "index.json"), "../index.json"):
            result, errors = self.run_cli(("index", "--output", unsafe))
            self.assertEqual(2, result)
            self.assertIn("context evidence path resolves outside the repository", errors)

    def test_select_rejects_outside_index_input_and_manifest_output(self):
        outside_index = str(Path(self.outside.name) / "index.json")
        result, _ = self.run_cli(
            ("select", "--story", "EFF-IDX-001", "--index", outside_index)
        )
        self.assertEqual(2, result)
        result, _ = self.run_cli(
            (
                "select",
                "--story",
                "EFF-IDX-001",
                "--output",
                str(Path(self.outside.name) / "manifest.json"),
            )
        )
        self.assertEqual(2, result)


class ValidationCliPathTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.outside = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.outside.cleanup()

    def run_cli(self, report):
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()) as errors:
            result = validation_main(
                ("--root", str(self.root), "--report", str(report))
            )
        return result, errors.getvalue()

    def test_validation_accepts_nested_repository_report(self):
        with tempfile.TemporaryDirectory(dir=str(self.root)) as directory:
            report = Path(directory) / "nested" / "report.json"
            result, _ = self.run_cli(report)
            self.assertEqual(0, result)
            self.assertTrue(report.is_file())

    def test_validation_rejects_absolute_outside_and_parent_report(self):
        for unsafe in (Path(self.outside.name) / "report.json", "../report.json"):
            result, errors = self.run_cli(unsafe)
            self.assertEqual(2, result)
            self.assertIn("validation evidence path resolves outside the repository", errors)


if __name__ == "__main__":
    unittest.main()
