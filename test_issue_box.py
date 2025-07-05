import unittest
from unittest.mock import patch
from main import JiraTrackerApp


class TestJiraTrackerApp(unittest.TestCase):

    @patch("main.get_key")
    def test_environment_variables_not_set(self, mock_get_key):
        # Simulate environment variables not being set
        mock_get_key.return_value = None

        # Initialize the app and check the returned widget
        app = JiraTrackerApp()
        widget = app.build()
        # Assert that JiraConnectionSettingsPopup is initialized when env vars are not set
        from jira_connection_settings_popup import JiraConnectionSettingsPopup

        self.assertIsInstance(widget, JiraConnectionSettingsPopup)

    @patch("main.get_key")
    def test_environment_variables_set(self, mock_get_key):
        # Simulate environment variables being set
        mock_get_key.return_value = "some_value"

        # Initialize the app and check the returned widget
        app = JiraTrackerApp()
        widget = app.build()
        # Assert that JiraIssueTracker is initialized when env vars are set
        from jira_issue_tracker import JiraIssueTracker

        self.assertIsInstance(widget, JiraIssueTracker)


if __name__ == "__main__":
    unittest.main()
