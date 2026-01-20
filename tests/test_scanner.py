import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.engine.scanner import Scanner

class TestScanner(unittest.TestCase):
    """Unit tests for the Scanner module."""

    def setUp(self):
        """Set up test fixtures."""
        self.scanner = Scanner(templates_dir="src/templates")

    def test_load_xss_patterns(self):
        """Test loading XSS patterns."""
        patterns = self.scanner.load_patterns("xss")
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
        self.assertIn("id", patterns[0])
        self.assertIn("payload", patterns[0])

    def test_load_sqli_patterns(self):
        """Test loading SQLi patterns."""
        patterns = self.scanner.load_patterns("sqli")
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
        self.assertIn("severity", patterns[0])

    def test_load_nonexistent_patterns(self):
        """Test loading non-existent pattern file."""
        patterns = self.scanner.load_patterns("nonexistent")
        self.assertEqual(patterns, [])

    def test_scanner_initialization(self):
        """Test scanner initializes correctly."""
        self.assertEqual(self.scanner.results, [])
        self.assertEqual(self.scanner.templates_dir, "src/templates")

    def test_generate_empty_report(self):
        """Test generating report with no results."""
        report = self.scanner.generate_report()
        self.assertEqual(report, "[]")


class TestSystemCheck(unittest.TestCase):
    """Unit tests for System Check module."""

    def test_import_system_check(self):
        """Test that system_check module imports correctly."""
        try:
            from src.utils.system_check import check_system
            self.assertTrue(callable(check_system))
        except ImportError as e:
            self.fail(f"Failed to import system_check: {e}")


if __name__ == "__main__":
    unittest.main()
