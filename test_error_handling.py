import unittest
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop
from kivymd.app import MDApp
from jira_issue_tracker import JiraIssueTracker
from jira_connection_settings_popup import JiraConnectionSettingsPopup


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
        app = MDApp()
        tracker = JiraIssueTracker()
        
        # Check that setup_ui was not called (no normal UI)
        self.assertEqual(len(tracker.children), 1)  # Only the error label
        self.assertIn("Error: Jira Site URL is not set", tracker.children[0].text)

    @patch('jira_issue_tracker.get_key', return_value='https://test-jira.com')
    def test_valid_jira_site_url_shows_normal_ui(self, mock_get_key):
        """Test that valid JIRA_SITE_URL shows normal UI."""
        app = MDApp()
        tracker = JiraIssueTracker()
        
        # Check that normal UI is shown (more than just error label)
        self.assertGreater(len(tracker.children), 1)

    @patch('api.get_key', return_value='')
    def test_empty_jql_queries_are_filtered_out(self, mock_get_key):
        """Test that empty JQL queries are filtered out and don't create boxes."""
        with patch('jira_issue_tracker.get_key', return_value='https://test-jira.com'):
            tracker = JiraIssueTracker()
            
            # With empty queries, no issue boxes should be created
            self.assertEqual(len(tracker.boxes), 0)

    @patch('api.get_key', return_value='project = TEST')
    def test_valid_jql_queries_create_boxes(self, mock_get_key):
        """Test that valid JQL queries create issue boxes."""
        with patch('jira_issue_tracker.get_key', return_value='https://test-jira.com'):
            tracker = JiraIssueTracker()
            
            # With valid queries, issue boxes should be created
            self.assertGreater(len(tracker.boxes), 0)

    @patch('api.get_jql_query_results', side_effect=Exception("API Error"))
    def test_api_error_handling_in_update_labels(self, mock_get_results):
        """Test that API errors in update_labels are handled gracefully."""
        with patch('jira_issue_tracker.get_key', return_value='https://test-jira.com'):
            tracker = JiraIssueTracker()
            
            # Mock a box with a query
            mock_box = MagicMock()
            mock_box.jql_query = "project = TEST"
            tracker.boxes = [mock_box]
            
            # Call update_labels and check that error is handled
            tracker.update_labels(0)
            
            # Verify that the box's update_label was called with error message
            mock_box.update_label.assert_called_with("Error fetching data")

    def test_settings_popup_initialization(self):
        """Test that settings popup initializes correctly."""
        popup = JiraConnectionSettingsPopup()
        
        # Check that popup has the expected structure
        self.assertIsNotNone(popup.content_cls)
        self.assertIsNotNone(popup.jira_site_url)
        self.assertIsNotNone(popup.jira_api_token)

    @patch('jira_connection_settings_popup.set_key')
    def test_settings_popup_save_functionality(self, mock_set_key):
        """Test that settings popup saves values correctly."""
        popup = JiraConnectionSettingsPopup()
        
        # Set test values
        popup.jira_site_url.text = "https://test-jira.com"
        popup.jira_api_token.text = "test-token"
        
        # Mock the app stop method
        with patch('jira_connection_settings_popup.MDApp.get_running_app') as mock_app:
            mock_app_instance = MagicMock()
            mock_app.return_value = mock_app_instance
            
            # Call save_settings
            popup.save_settings(None)
            
            # Verify that set_key was called with correct values
            mock_set_key.assert_any_call('.env', 'JIRA_SITE_URL', 'https://test-jira.com')
            mock_set_key.assert_any_call('.env', 'JIRA_API_TOKEN', 'test-token')


if __name__ == '__main__':
    unittest.main() 