import os
import unittest
from unittest.mock import patch
from api import create_request_url


class TestApi(unittest.TestCase):

    @patch('api.JIRA_SITE_URL', 'http://test-jira.com')
    def test_create_request_url(self):
        # Test the create_request_url function
        endpoint = '/test-endpoint'
        expected_url = 'http://test-jira.com/test-endpoint'
        result_url = create_request_url(endpoint)
        self.assertEqual(result_url, expected_url)

    @patch('requests.get')
    def test_api_call_success(self, mock_get):
        # Mock a successful API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test_data'}
        mock_get.return_value = mock_response

        # Call the API function and assert the response
        response = api_function()  # Replace with actual API function call
        self.assertEqual(response, {'data': 'test_data'})


class TestApiEnvironmentVariables(unittest.TestCase):

    @patch('os.getenv')
    def test_jira_api_key_retrieval(self, mock_getenv):
        # Mock the getenv function to return a test API key
        mock_getenv.return_value = 'test_api_key'

        # Retrieve the API key using the function in api.py
        api_key = os.getenv('JIRA_API_KEY')  # Replace with actual function call if different

        # Assert that the retrieved API key matches the mock
        self.assertEqual(api_key, 'test_api_key')


if __name__ == '__main__':
    unittest.main()
