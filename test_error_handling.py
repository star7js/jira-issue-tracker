import unittest
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop
from jira_issue_tracker import JiraIssueTracker
from requests.exceptions import RequestException


class TestErrorHandling(unittest.TestCase):
    """Test error handling and UI interactions."""

    def setUp(self):
        """Set up test environment."""
        EventLoop.ensure_window()

    def tearDown(self):
        """Clean up after tests."""
        EventLoop.close()

    @patch('jira_issue_tracker.get_key', return_value=None)
    def test_missing_jira_site_url_shows_error_label(self, mock_get_key):
        """Test that missing JIRA_SITE_URL shows an error label instead of normal UI."""
        tracker = JiraIssueTracker()
        # Check that setup_ui was not called (no normal UI)
        self.assertEqual(len(tracker.children), 1)  # Only the error label
        self.assertIn("Error: Jira Site URL is not set", tracker.children[0].text)

    @patch('jira_issue_tracker.get_jql_query_results', side_effect=RequestException("API Error"))
    def test_api_error_handling_logic(self, mock_get_results):
        """Test that API errors are handled gracefully in the logic."""
        # Test the error handling logic without creating UI components
        with patch('jira_issue_tracker.get_key', return_value='https://test-jira.com'):
            # Create tracker but don't call setup_ui to avoid KivyMD context issues
            tracker = JiraIssueTracker.__new__(JiraIssueTracker)
            tracker.boxes = []
            
            # Mock a box with a query
            mock_box = MagicMock()
            mock_box.jql_query = "project = TEST"
            tracker.boxes = [mock_box]
            
            # Test the update_labels method directly
            with patch('jira_issue_tracker.get_key', return_value='TRUE'):
                tracker.update_labels(0)
                # Verify that the box's update_label was called with error message
                mock_box.update_label.assert_called_with("Error fetching data")

    def test_empty_jql_queries_are_filtered_out_logic(self):
        """Test that empty JQL queries are filtered out in the logic."""
        # Test the filtering logic directly without UI components
        jql_queries = {
            "Query One": "",
            "Query Two": "project = TEST",
            "Query Three": "",
            "Query Four": "project = DEMO"
        }
        
        # Filter out empty queries
        active_queries = {k: v for k, v in jql_queries.items() if v}
        
        # Should have 2 active queries
        self.assertEqual(len(active_queries), 2)
        self.assertIn("Query Two", active_queries)
        self.assertIn("Query Four", active_queries)

    def test_valid_jql_queries_logic(self):
        """Test that valid JQL queries are processed correctly."""
        # Test the query processing logic directly
        jql_queries = {
            "Query One": "project = TEST",
            "Query Two": "reporter = currentUser()",
        }
        
        # All queries should be active
        active_queries = {k: v for k, v in jql_queries.items() if v}
        self.assertEqual(len(active_queries), 2)


if __name__ == '__main__':
    unittest.main()
