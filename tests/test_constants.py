import unittest
from jira_tracker import api, security, env_validator


class TestConstants(unittest.TestCase):
    """Test that all module constants are properly defined."""

    def test_api_timeouts(self):
        """Test API timeout constants"""
        self.assertEqual(api.DEFAULT_API_REQUEST_INTERVAL, 3600)
        self.assertEqual(api.DEFAULT_REQUEST_TIMEOUT, 10)

    def test_api_endpoints(self):
        """Test API endpoint constants"""
        self.assertIn("/rest/api/3/", api.JIRA_API_ENDPOINT_CLOUD)
        self.assertIn("/rest/api/2/", api.JIRA_API_ENDPOINT_SERVER)

    def test_security_constants(self):
        """Test security module constants"""
        self.assertEqual(security.DEFAULT_REQUEST_TIMEOUT, 10)
        self.assertEqual(security.RETRY_TOTAL, 3)
        self.assertEqual(security.RETRY_BACKOFF_FACTOR, 1)
        self.assertIsInstance(security.RETRY_STATUS_CODES, list)
        self.assertGreater(len(security.RETRY_STATUS_CODES), 0)

    def test_env_validator_required_vars(self):
        """Test required environment variables list"""
        self.assertIn("JIRA_SITE_URL", env_validator.REQUIRED_ENV_VARS)
        self.assertIn("JIRA_API_TOKEN", env_validator.REQUIRED_ENV_VARS)
        self.assertEqual(len(env_validator.REQUIRED_ENV_VARS), 2)

    def test_env_validator_optional_vars(self):
        """Test optional environment variables list"""
        self.assertIn("JIRA_EMAIL", env_validator.OPTIONAL_ENV_VARS)
        self.assertIn("JQL_QUERY_ONE", env_validator.OPTIONAL_ENV_VARS)
        self.assertIn("THEME_PREFERENCE", env_validator.OPTIONAL_ENV_VARS)
        self.assertGreater(len(env_validator.OPTIONAL_ENV_VARS), 3)

    def test_api_module_has_safe_requests_import(self):
        """Test that api module imports safe_requests"""
        self.assertTrue(hasattr(api, "safe_requests"))

    def test_api_module_has_logger(self):
        """Test that api module has logger configured"""
        self.assertTrue(hasattr(api, "logger"))

    def test_security_module_has_safe_requests_instance(self):
        """Test that security module exposes safe_requests instance"""
        self.assertTrue(hasattr(security, "safe_requests"))
        self.assertIsNotNone(security.safe_requests)

    def test_env_validator_has_logger(self):
        """Test that env_validator module has logger configured"""
        self.assertTrue(hasattr(env_validator, "logger"))


if __name__ == "__main__":
    unittest.main()
