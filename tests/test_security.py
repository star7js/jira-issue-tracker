import unittest
from unittest.mock import patch, MagicMock
import requests
from jira_tracker.security import SafeRequests


class TestSafeRequests(unittest.TestCase):

    def setUp(self):
        self.safe_requests = SafeRequests()

    def test_safe_requests_get_invalid_url(self):
        """Test that invalid URLs raise ValueError"""
        with self.assertRaises(ValueError):
            self.safe_requests.get("")
        with self.assertRaises(ValueError):
            self.safe_requests.get(None)

    @patch("jira_tracker.security.logger")
    def test_safe_requests_get_http_warning(self, mock_logger):
        """Test that HTTP non-localhost URLs log warning"""
        with patch.object(self.safe_requests.session, "get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            self.safe_requests.get("http://example.com")
            mock_logger.warning.assert_called_once()
            self.assertIn("HTTP instead of HTTPS", mock_logger.warning.call_args[0][0])

    @patch("jira_tracker.security.logger")
    def test_safe_requests_get_request_exception(self, mock_logger):
        """Test that RequestException is re-raised after logging"""
        with patch.object(self.safe_requests.session, "get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
            with self.assertRaises(requests.exceptions.ConnectionError):
                self.safe_requests.get("https://example.com")
            mock_logger.error.assert_called_once()
            self.assertIn("Request failed", mock_logger.error.call_args[0][0])

    @patch("jira_tracker.security.logger")
    def test_safe_requests_get_generic_exception(self, mock_logger):
        """Test that generic exceptions are re-raised after logging"""
        with patch.object(self.safe_requests.session, "get") as mock_get:
            mock_get.side_effect = Exception("Unexpected error")
            with self.assertRaises(Exception):
                self.safe_requests.get("https://example.com")
            mock_logger.error.assert_called_once()
            self.assertIn("Unexpected error", mock_logger.error.call_args[0][0])

    def test_safe_requests_post_success(self):
        """Test successful POST request"""
        with patch.object(self.safe_requests.session, "post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200, json=lambda: {"result": "success"})
            response = self.safe_requests.post("https://example.com", json={"key": "value"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"result": "success"})

    def test_safe_requests_post_invalid_url(self):
        """Test that invalid URLs raise ValueError"""
        with self.assertRaises(ValueError):
            self.safe_requests.post("")
        with self.assertRaises(ValueError):
            self.safe_requests.post(None)

    @patch("jira_tracker.security.logger")
    def test_safe_requests_post_request_exception(self, mock_logger):
        """Test that RequestException is re-raised after logging"""
        with patch.object(self.safe_requests.session, "post") as mock_post:
            mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
            with self.assertRaises(requests.exceptions.Timeout):
                self.safe_requests.post("https://example.com", json={"key": "value"})
            mock_logger.error.assert_called_once()
            self.assertIn("Request failed", mock_logger.error.call_args[0][0])

    @patch("jira_tracker.security.logger")
    def test_safe_requests_post_generic_exception(self, mock_logger):
        """Test that generic exceptions are re-raised after logging"""
        with patch.object(self.safe_requests.session, "post") as mock_post:
            mock_post.side_effect = Exception("Unexpected error")
            with self.assertRaises(Exception):
                self.safe_requests.post("https://example.com", json={"key": "value"})
            mock_logger.error.assert_called_once()
            self.assertIn("Unexpected error", mock_logger.error.call_args[0][0])

    def test_safe_requests_get_localhost_http_no_warning(self):
        """Test that HTTP localhost URLs don't trigger warning"""
        with patch.object(self.safe_requests.session, "get") as mock_get:
            with patch("jira_tracker.security.logger") as mock_logger:
                mock_get.return_value = MagicMock(status_code=200)
                self.safe_requests.get("http://localhost:8080")
                # Should not log warning for localhost
                mock_logger.warning.assert_not_called()

    def test_safe_requests_get_127_http_no_warning(self):
        """Test that HTTP 127.0.0.1 URLs don't trigger warning"""
        with patch.object(self.safe_requests.session, "get") as mock_get:
            with patch("jira_tracker.security.logger") as mock_logger:
                mock_get.return_value = MagicMock(status_code=200)
                self.safe_requests.get("http://127.0.0.1:8080")
                # Should not log warning for 127.0.0.1
                mock_logger.warning.assert_not_called()

    def test_safe_requests_session_has_retry_strategy(self):
        """Test that session has retry adapters mounted"""
        self.assertIsNotNone(self.safe_requests.session)
        # Check that adapters are mounted
        self.assertIn("http://", self.safe_requests.session.adapters)
        self.assertIn("https://", self.safe_requests.session.adapters)

    def test_default_request_timeout_constant(self):
        """Test that default timeout constant is defined"""
        from jira_tracker.security import DEFAULT_REQUEST_TIMEOUT
        self.assertEqual(DEFAULT_REQUEST_TIMEOUT, 10)

    def test_retry_constants(self):
        """Test that retry constants are properly defined"""
        from jira_tracker.security import RETRY_TOTAL, RETRY_BACKOFF_FACTOR, RETRY_STATUS_CODES
        self.assertEqual(RETRY_TOTAL, 3)
        self.assertEqual(RETRY_BACKOFF_FACTOR, 1)
        self.assertEqual(RETRY_STATUS_CODES, [429, 500, 502, 503, 504])

    def test_safe_requests_post_with_data(self):
        """Test POST request with data parameter"""
        with patch.object(self.safe_requests.session, "post") as mock_post:
            mock_post.return_value = MagicMock(status_code=201)
            response = self.safe_requests.post("https://example.com", data="test data")
            self.assertEqual(response.status_code, 201)
            mock_post.assert_called_once()

    def test_safe_requests_get_with_params(self):
        """Test GET request with params"""
        with patch.object(self.safe_requests.session, "get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            response = self.safe_requests.get("https://example.com", params={"key": "value"})
            self.assertEqual(response.status_code, 200)
            call_kwargs = mock_get.call_args[1]
            self.assertEqual(call_kwargs["params"], {"key": "value"})


if __name__ == "__main__":
    unittest.main()
