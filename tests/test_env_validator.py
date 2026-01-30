import unittest
from unittest.mock import patch, mock_open
import os
from jira_tracker.env_validator import validate_env_file, validate_jira_url


class TestEnvValidator(unittest.TestCase):

    @patch("os.path.exists")
    def test_validate_env_file_not_exists(self, mock_exists):
        """Test validation fails when .env file doesn't exist"""
        mock_exists.return_value = False
        is_valid, missing = validate_env_file()
        self.assertFalse(is_valid)
        self.assertIn("File .env does not exist", missing)

    @patch("os.access")
    @patch("os.path.exists")
    def test_validate_env_file_not_readable(self, mock_exists, mock_access):
        """Test validation fails when .env file is not readable"""
        mock_exists.return_value = True
        mock_access.return_value = False
        is_valid, missing = validate_env_file()
        self.assertFalse(is_valid)
        self.assertIn("File .env is not readable", missing)

    @patch("dotenv.get_key")
    @patch("dotenv.load_dotenv")
    @patch("os.access")
    @patch("os.path.exists")
    def test_validate_env_file_missing_vars(
        self, mock_exists, mock_access, mock_load, mock_get_key
    ):
        """Test validation fails when required variables are missing"""
        mock_exists.return_value = True
        mock_access.return_value = True

        def get_key_side_effect(path, key):
            if key == "JIRA_SITE_URL":
                return ""
            elif key == "JIRA_API_TOKEN":
                return None
            return None

        mock_get_key.side_effect = get_key_side_effect
        is_valid, missing = validate_env_file()
        self.assertFalse(is_valid)
        self.assertIn("JIRA_SITE_URL", missing)
        self.assertIn("JIRA_API_TOKEN", missing)

    def test_validate_jira_url_empty(self):
        """Test validation rejects empty URL"""
        self.assertFalse(validate_jira_url(""))
        self.assertFalse(validate_jira_url(None))

    def test_validate_jira_url_no_protocol(self):
        """Test validation rejects URL without protocol"""
        self.assertFalse(validate_jira_url("example.com"))
        self.assertFalse(validate_jira_url("jira.example.com"))

    def test_validate_jira_url_trailing_slash(self):
        """Test validation rejects URL with trailing slash"""
        self.assertFalse(validate_jira_url("https://example.com/"))
        self.assertFalse(validate_jira_url("http://jira.example.com/"))

    def test_validate_jira_url_valid(self):
        """Test validation accepts valid URLs"""
        valid_urls = [
            "https://example.com",
            "http://localhost:8080",
            "https://jira.example.com",
            "https://example.atlassian.net",
            "http://127.0.0.1:8080",
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(validate_jira_url(url))

    @patch("dotenv.get_key")
    @patch("dotenv.load_dotenv")
    @patch("os.access")
    @patch("os.path.exists")
    def test_validate_env_file_success(
        self, mock_exists, mock_access, mock_load, mock_get_key
    ):
        """Test validation succeeds with all required variables"""
        mock_exists.return_value = True
        mock_access.return_value = True

        def get_key_side_effect(path, key):
            if key == "JIRA_SITE_URL":
                return "https://jira.example.com"
            elif key == "JIRA_API_TOKEN":
                return "test-token-123"
            return None

        mock_get_key.side_effect = get_key_side_effect
        is_valid, missing = validate_env_file()
        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    @patch("dotenv.get_key")
    @patch("dotenv.load_dotenv")
    @patch("os.access")
    @patch("os.path.exists")
    def test_validate_env_file_whitespace_values(
        self, mock_exists, mock_access, mock_load, mock_get_key
    ):
        """Test validation fails with whitespace-only values"""
        mock_exists.return_value = True
        mock_access.return_value = True

        def get_key_side_effect(path, key):
            if key == "JIRA_SITE_URL":
                return "   "
            elif key == "JIRA_API_TOKEN":
                return "\t\n"
            return None

        mock_get_key.side_effect = get_key_side_effect
        is_valid, missing = validate_env_file()
        self.assertFalse(is_valid)
        self.assertEqual(len(missing), 2)

    def test_required_env_vars_constant(self):
        """Test that REQUIRED_ENV_VARS constant is defined"""
        from jira_tracker.env_validator import REQUIRED_ENV_VARS
        self.assertIsInstance(REQUIRED_ENV_VARS, list)
        self.assertIn("JIRA_SITE_URL", REQUIRED_ENV_VARS)
        self.assertIn("JIRA_API_TOKEN", REQUIRED_ENV_VARS)

    def test_optional_env_vars_constant(self):
        """Test that OPTIONAL_ENV_VARS constant is defined"""
        from jira_tracker.env_validator import OPTIONAL_ENV_VARS
        self.assertIsInstance(OPTIONAL_ENV_VARS, list)
        self.assertIn("JIRA_EMAIL", OPTIONAL_ENV_VARS)


if __name__ == "__main__":
    unittest.main()
