import unittest
from unittest.mock import patch, MagicMock
import api


class TestJiraAPIProgram(unittest.TestCase):

    @patch("api.load_dotenv")
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

    @patch("api.safe_requests.get")
    def test_execute_request_server_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"total": 42})
        response = api.execute_request_server("http://test.com", {}, {})
        self.assertIsNotNone(response)
        self.assertEqual(response, {"total": 42})

    @patch("api.safe_requests.get")
    def test_execute_request_server_failure(self, mock_get):
        mock_get.side_effect = api.requests.HTTPError()
        response = api.execute_request_server("http://test.com", {}, {})
        self.assertIsNone(response)

    # Add more tests for handle_request_error, get_jql_query_results, etc.


if __name__ == "__main__":
    unittest.main()
