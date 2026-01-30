import unittest
from unittest.mock import patch, MagicMock
from jira_tracker.main import JiraTrackerApp


class TestJiraTrackerApp(unittest.TestCase):

    @patch("jira_tracker.main.get_key")
    def test_environment_variables_not_set(self, mock_get_key):
        # Simulate environment variables not being set
        mock_get_key.return_value = None

        # Test the logic without creating actual widgets
        with patch("jira_tracker.main.JiraConnectionSettingsPopup") as mock_popup:
            mock_widget = MagicMock()
            mock_popup.return_value = mock_widget

            app = JiraTrackerApp()
            widget = app.build()

            # Verify the correct widget was created
            mock_popup.assert_called_once()
            self.assertEqual(widget, mock_widget)

    @patch("jira_tracker.main.validate_jira_url")
    @patch("jira_tracker.main.validate_env_file")
    @patch("jira_tracker.main.get_key")
    def test_environment_variables_set(
        self, mock_get_key, mock_validate_env, mock_validate_url
    ):
        # Simulate environment variables being set and validation passing
        mock_get_key.return_value = "https://jira.example.com"
        mock_validate_env.return_value = (True, [])
        mock_validate_url.return_value = True

        # Test the logic without creating actual widgets
        with patch("jira_tracker.main.JiraIssueTracker") as mock_tracker:
            mock_widget = MagicMock()
            mock_tracker.return_value = mock_widget

            app = JiraTrackerApp()
            widget = app.build()

            # Verify the correct widget was created
            mock_tracker.assert_called_once()
            self.assertEqual(widget, mock_widget)

    @patch("jira_tracker.main.validate_jira_url")
    @patch("jira_tracker.main.validate_env_file")
    @patch("jira_tracker.main.get_key")
    def test_invalid_jira_url(
        self, mock_get_key, mock_validate_env, mock_validate_url
    ):
        """Test that invalid Jira URL returns settings popup"""
        mock_get_key.return_value = "invalid-url"
        mock_validate_env.return_value = (True, [])
        mock_validate_url.return_value = False

        with patch("jira_tracker.main.JiraConnectionSettingsPopup") as mock_popup:
            mock_widget = MagicMock()
            mock_popup.return_value = mock_widget

            app = JiraTrackerApp()
            widget = app.build()

            mock_popup.assert_called_once()
            self.assertEqual(widget, mock_widget)

    def test_jira_tracker_app_title(self):
        """Test that JiraTrackerApp has correct title"""
        app = JiraTrackerApp()
        self.assertEqual(app.title, "Jira Tracker")

    def test_jira_tracker_app_icon(self):
        """Test that JiraTrackerApp has correct icon"""
        app = JiraTrackerApp()
        self.assertEqual(app.icon, "icon.png")

    @patch("jira_tracker.main.validate_jira_url")
    @patch("jira_tracker.main.validate_env_file")
    def test_build_sets_theme_when_theme_cls_exists(
        self, mock_validate_env, mock_validate_url
    ):
        """Test that build() sets theme when theme_cls attribute exists"""
        mock_validate_env.return_value = (True, [])
        mock_validate_url.return_value = True

        with patch("jira_tracker.main.get_key", return_value="https://jira.example.com"):
            with patch("jira_tracker.main.JiraIssueTracker") as mock_tracker:
                mock_widget = MagicMock()
                mock_tracker.return_value = mock_widget

                app = JiraTrackerApp()
                app.theme_cls = MagicMock()

                widget = app.build()

                self.assertEqual(app.theme_cls.theme_style, "Dark")
                self.assertEqual(app.theme_cls.primary_palette, "DeepPurple")
                self.assertEqual(app.theme_cls.accent_palette, "Cyan")


if __name__ == "__main__":
    unittest.main()
