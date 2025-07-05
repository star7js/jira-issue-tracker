import unittest
from unittest.mock import patch, MagicMock
from main import JiraTrackerApp


class TestJiraTrackerApp(unittest.TestCase):

    @patch("main.get_key")
    def test_environment_variables_not_set(self, mock_get_key):
        # Simulate environment variables not being set
        mock_get_key.return_value = None

        # Test the logic without creating actual widgets
        with patch('main.JiraConnectionSettingsPopup') as mock_popup:
            mock_widget = MagicMock()
            mock_popup.return_value = mock_widget
            
            app = JiraTrackerApp()
            widget = app.build()
            
            # Verify the correct widget was created
            mock_popup.assert_called_once()
            self.assertEqual(widget, mock_widget)

    @patch("main.get_key")
    def test_environment_variables_set(self, mock_get_key):
        # Simulate environment variables being set
        mock_get_key.return_value = "some_value"

        # Test the logic without creating actual widgets
        with patch('main.JiraIssueTracker') as mock_tracker:
            mock_widget = MagicMock()
            mock_tracker.return_value = mock_widget
            
            app = JiraTrackerApp()
            widget = app.build()
            
            # Verify the correct widget was created
            mock_tracker.assert_called_once()
            self.assertEqual(widget, mock_widget)


if __name__ == "__main__":
    unittest.main()
