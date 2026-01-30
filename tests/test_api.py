import unittest
from unittest.mock import patch, MagicMock
from jira_tracker import api


class TestJiraAPIProgram(unittest.TestCase):

    @patch("jira_tracker.api.load_dotenv")
    def test_load_env_variables(self, mock_load_dotenv):
        api.load_dotenv()
        mock_load_dotenv.assert_called_once()

    def test_create_request_url(self):
        test_endpoint = "/test"
        expected_url = f"{api.JIRA_SITE_URL}{test_endpoint}"
        self.assertEqual(api.create_request_url(test_endpoint), expected_url)

    def test_create_request_headers_server(self):
        expected_headers = {"Authorization": f"Bearer {api.JIRA_API_TOKEN}"}
        self.assertEqual(api.create_request_headers_server(), expected_headers)

    @patch("jira_tracker.api.safe_requests.get")
    def test_execute_request_server_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"total": 42})
        response = api.execute_request_server("http://test.com", {}, {})
        self.assertIsNotNone(response)
        self.assertEqual(response, {"total": 42})

    @patch("jira_tracker.api.safe_requests.get")
    def test_execute_request_server_failure(self, mock_get):
        mock_get.side_effect = api.requests.HTTPError()
        response = api.execute_request_server("http://test.com", {}, {})
        self.assertIsNone(response)

    def test_create_request_headers_cloud(self):
        """Test cloud authentication with base64 encoding"""
        headers = api.create_request_headers_cloud()
        self.assertIn("Authorization", headers)
        self.assertTrue(headers["Authorization"].startswith("Basic "))
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("jira_tracker.api.safe_requests.post")
    def test_execute_request_cloud_success(self, mock_post):
        """Test successful cloud request execution"""
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"count": 42})
        response = api.execute_request_cloud("http://test.com", {}, "project = TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, {"count": 42})
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]["json"], {"jql": "project = TEST"})

    @patch("jira_tracker.api.safe_requests.post")
    def test_execute_request_cloud_failure(self, mock_post):
        """Test cloud request failure handling"""
        mock_post.side_effect = api.requests.HTTPError()
        response = api.execute_request_cloud("http://test.com", {}, "project = TEST")
        self.assertIsNone(response)

    @patch("jira_tracker.api.logger")
    def test_handle_request_error_connection_error(self, mock_logger):
        """Test connection error handling"""
        error = api.requests.ConnectionError()
        api.handle_request_error(error)
        mock_logger.error.assert_called_once_with("Failed to connect to the server.")

    @patch("jira_tracker.api.logger")
    def test_handle_request_error_timeout(self, mock_logger):
        """Test timeout error handling"""
        error = api.requests.Timeout()
        api.handle_request_error(error)
        mock_logger.error.assert_called_once_with("Request timed out.")

    @patch("jira_tracker.api.logger")
    def test_handle_request_error_too_many_redirects(self, mock_logger):
        """Test too many redirects error handling"""
        error = api.requests.TooManyRedirects()
        api.handle_request_error(error)
        mock_logger.error.assert_called_once_with("Too many redirects.")

    @patch("jira_tracker.api.logger")
    def test_handle_request_error_generic(self, mock_logger):
        """Test generic error handling"""
        error = api.requests.RequestException("Something went wrong")
        api.handle_request_error(error)
        mock_logger.error.assert_called_once()
        self.assertIn("An error occurred", mock_logger.error.call_args[0][0])

    @patch("jira_tracker.api.logger")
    def test_handle_request_error_http_error(self, mock_logger):
        """Test HTTP error handling"""
        error = api.requests.HTTPError("404 Not Found")
        api.handle_request_error(error)
        mock_logger.error.assert_called_once()
        self.assertIn("HTTP error", mock_logger.error.call_args[0][0])

    def test_validate_jql_query_empty_string(self):
        """Test validation rejects empty string"""
        self.assertFalse(api.validate_jql_query(""))

    def test_validate_jql_query_non_string(self):
        """Test validation rejects non-string input"""
        self.assertFalse(api.validate_jql_query(None))
        self.assertFalse(api.validate_jql_query(123))
        self.assertFalse(api.validate_jql_query(42))
        self.assertFalse(api.validate_jql_query(0))
        self.assertFalse(api.validate_jql_query([]))
        self.assertFalse(api.validate_jql_query(["project = TEST"]))

    def test_validate_jql_query_whitespace_only(self):
        """Test validation rejects whitespace-only strings"""
        self.assertFalse(api.validate_jql_query("   "))
        self.assertFalse(api.validate_jql_query("\t\n"))

    def test_validate_jql_query_suspicious_patterns(self):
        """Test validation rejects queries with suspicious patterns"""
        suspicious_queries = [
            "project = TEST'; DROP TABLE users",
            "project = TEST -- comment",
            "project = TEST /* comment */",
            "project = TEST */ badcode /*",
            "project = TEST xp_cmdshell",
            "project = TEST exec('malicious')",
            "project = TEST eval(bad_code)",
            "project = TEST XP_CMDSHELL",
            "project = TEST EXEC('code')",
            "project = TEST EVAL(code)",
        ]
        for query in suspicious_queries:
            with self.subTest(query=query):
                self.assertFalse(api.validate_jql_query(query))

    def test_validate_jql_query_valid(self):
        """Test validation accepts valid JQL queries"""
        valid_queries = [
            "project = TEST",
            "status = 'In Progress' AND assignee = currentUser()",
            "created >= -7d",
        ]
        for query in valid_queries:
            with self.subTest(query=query):
                self.assertTrue(api.validate_jql_query(query))

    @patch("jira_tracker.api.validate_jql_query")
    def test_get_jql_query_results_invalid_query(self, mock_validate):
        """Test get_jql_query_results with invalid query"""
        mock_validate.return_value = False
        result = api.get_jql_query_results("'; DROP TABLE")
        self.assertEqual(result, 0)

    @patch("jira_tracker.api.JIRA_EMAIL", "test@example.com")
    @patch("jira_tracker.api.execute_request_cloud")
    @patch("jira_tracker.api.create_request_headers_cloud")
    @patch("jira_tracker.api.create_request_url")
    def test_get_jql_query_results_cloud_path(
        self, mock_url, mock_headers, mock_execute
    ):
        """Test cloud path in get_jql_query_results"""
        mock_url.return_value = "http://test.com/api"
        mock_headers.return_value = {"Authorization": "Basic test"}
        mock_execute.return_value = {"count": 15}
        result = api.get_jql_query_results("project = TEST")
        self.assertEqual(result, 15)
        mock_execute.assert_called_once()

    @patch("jira_tracker.api.JIRA_EMAIL", "")
    @patch("jira_tracker.api.execute_request_server")
    @patch("jira_tracker.api.create_request_headers_server")
    @patch("jira_tracker.api.create_request_url")
    def test_get_jql_query_results_server_path(
        self, mock_url, mock_headers, mock_execute
    ):
        """Test server path in get_jql_query_results"""
        mock_url.return_value = "http://test.com/api"
        mock_headers.return_value = {"Authorization": "Bearer test"}
        mock_execute.return_value = {"total": 25}
        result = api.get_jql_query_results("project = TEST")
        self.assertEqual(result, 25)
        mock_execute.assert_called_once()

    @patch("jira_tracker.api.JIRA_EMAIL", "test@example.com")
    @patch("jira_tracker.api.execute_request_cloud")
    @patch("jira_tracker.api.create_request_headers_cloud")
    @patch("jira_tracker.api.create_request_url")
    def test_get_jql_query_results_null_response(
        self, mock_url, mock_headers, mock_execute
    ):
        """Test null response handling"""
        mock_url.return_value = "http://test.com/api"
        mock_headers.return_value = {"Authorization": "Basic test"}
        mock_execute.return_value = None
        result = api.get_jql_query_results("project = TEST")
        self.assertEqual(result, 0)

    @patch("jira_tracker.api.JIRA_EMAIL", "")
    @patch("jira_tracker.api.execute_request_server")
    @patch("jira_tracker.api.create_request_headers_server")
    @patch("jira_tracker.api.create_request_url")
    def test_get_jql_query_results_server_missing_total(
        self, mock_url, mock_headers, mock_execute
    ):
        """Test server response without total field"""
        mock_url.return_value = "http://test.com/api"
        mock_headers.return_value = {"Authorization": "Bearer test"}
        mock_execute.return_value = {"issues": []}
        result = api.get_jql_query_results("project = TEST")
        self.assertEqual(result, 0)

    @patch("jira_tracker.api.JIRA_EMAIL", "test@example.com")
    @patch("jira_tracker.api.execute_request_cloud")
    @patch("jira_tracker.api.create_request_headers_cloud")
    @patch("jira_tracker.api.create_request_url")
    def test_get_jql_query_results_cloud_missing_count(
        self, mock_url, mock_headers, mock_execute
    ):
        """Test cloud response without count field"""
        mock_url.return_value = "http://test.com/api"
        mock_headers.return_value = {"Authorization": "Basic test"}
        mock_execute.return_value = {"other_field": "value"}
        result = api.get_jql_query_results("project = TEST")
        self.assertEqual(result, 0)

    def test_default_constants(self):
        """Test that default constants are properly defined"""
        self.assertEqual(api.DEFAULT_API_REQUEST_INTERVAL, 3600)
        self.assertEqual(api.DEFAULT_REQUEST_TIMEOUT, 10)
        self.assertEqual(
            api.JIRA_API_ENDPOINT_CLOUD, "/rest/api/3/search/approximate-count"
        )
        self.assertEqual(api.JIRA_API_ENDPOINT_SERVER, "/rest/api/2/search")

    def test_jira_global_constants_exist(self):
        """Test that JIRA configuration constants are defined"""
        self.assertIsNotNone(hasattr(api, "JIRA_SITE_URL"))
        self.assertIsNotNone(hasattr(api, "JIRA_EMAIL"))
        self.assertIsNotNone(hasattr(api, "JIRA_API_TOKEN"))

    def test_jql_query_constants_exist(self):
        """Test that JQL query constants are defined"""
        self.assertIsNotNone(hasattr(api, "JQL_QUERY_ONE"))
        self.assertIsNotNone(hasattr(api, "JQL_QUERY_TWO"))
        self.assertIsNotNone(hasattr(api, "JQL_QUERY_THREE"))
        self.assertIsNotNone(hasattr(api, "JQL_QUERY_FOUR"))

    @patch("jira_tracker.api.safe_requests.get")
    def test_execute_request_server_with_raise_for_status(self, mock_get):
        """Test that execute_request_server calls raise_for_status"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"total": 10}
        mock_get.return_value = mock_response

        api.execute_request_server("http://test.com", {}, {})

        mock_response.raise_for_status.assert_called_once()

    @patch("jira_tracker.api.safe_requests.post")
    def test_execute_request_cloud_with_raise_for_status(self, mock_post):
        """Test that execute_request_cloud calls raise_for_status"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"count": 10}
        mock_post.return_value = mock_response

        api.execute_request_cloud("http://test.com", {}, "project = TEST")

        mock_response.raise_for_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()
