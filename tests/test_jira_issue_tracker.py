import unittest
from unittest.mock import patch, MagicMock
from jira_tracker.jira_issue_tracker import JiraIssueTracker


class TestJiraIssueTracker(unittest.TestCase):

    @patch(
        "jira_tracker.jira_issue_tracker.get_key",
        return_value="https://dummy-jira-url.com",
    )
    def test_initialization(self, mock_get_key):
        # Test initialization without creating Kivy window or app
        with patch("jira_tracker.jira_issue_tracker.MDLabel") as mock_mdlabel:
            mock_label = MagicMock()
            mock_mdlabel.return_value = mock_label

            with patch.object(JiraIssueTracker, "setup_ui") as mock_setup_ui:
                with patch.object(JiraIssueTracker, "add_widget") as mock_add_widget:
                    tracker = JiraIssueTracker()

                    # Verify initialization
                    self.assertEqual(
                        tracker.jira_site_url, "https://dummy-jira-url.com"
                    )
                    self.assertEqual(
                        tracker.jira_base_url, "https://dummy-jira-url.com/issues/"
                    )
                    self.assertIsInstance(tracker.boxes, list)

                    # Verify setup_ui was called
                    mock_setup_ui.assert_called_once()

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value=None)
    def test_initialization_no_url(self, mock_get_key):
        """Test initialization when JIRA URL is not set"""
        with patch("jira_tracker.jira_issue_tracker.MDLabel") as mock_mdlabel:
            mock_label = MagicMock()
            mock_mdlabel.return_value = mock_label

            with patch.object(JiraIssueTracker, "setup_ui") as mock_setup_ui:
                with patch.object(JiraIssueTracker, "add_widget") as mock_add_widget:
                    tracker = JiraIssueTracker()
                    mock_add_widget.assert_called_once()
                    mock_setup_ui.assert_not_called()

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_create_issue_box(self, mock_get_key):
        """Test creating an issue box"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget") as mock_add_widget:
                with patch("jira_tracker.jira_issue_tracker.IssueBox") as mock_issue_box:
                    tracker = JiraIssueTracker()
                    tracker.boxes = []

                    mock_box = MagicMock()
                    mock_issue_box.return_value = mock_box

                    tracker.create_issue_box("Test Title", "project = TEST")

                    mock_issue_box.assert_called_once()
                    self.assertEqual(len(tracker.boxes), 1)

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_create_empty_box(self, mock_get_key):
        """Test creating an empty box"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget") as mock_add_widget:
                with patch("jira_tracker.jira_issue_tracker.IssueBox") as mock_issue_box:
                    tracker = JiraIssueTracker()
                    tracker.jira_base_url = "https://dummy-jira-url.com/issues/"

                    mock_box = MagicMock()
                    mock_issue_box.return_value = mock_box

                    tracker.create_empty_box()

                    mock_issue_box.assert_called_once_with(
                        title="", jql_query="", jira_base_url="https://dummy-jira-url.com/issues/"
                    )
                    self.assertTrue(mock_box.disabled)

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_create_issue_boxes_single_query(self, mock_get_key):
        """Test creating issue boxes with a single query"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_ONE", "project = ONE"):
                    with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_TWO", ""):
                        with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_THREE", ""):
                            with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_FOUR", ""):
                                tracker = JiraIssueTracker()
                                tracker.boxes = []

                                with patch.object(tracker, "create_issue_box") as mock_create:
                                    tracker.create_issue_boxes()

                                    self.assertEqual(tracker.cols, 1)
                                    self.assertEqual(mock_create.call_count, 1)

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_create_issue_boxes_multiple_queries(self, mock_get_key):
        """Test creating issue boxes with multiple queries"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_ONE", "project = ONE"):
                    with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_TWO", "project = TWO"):
                        with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_THREE", ""):
                            with patch("jira_tracker.jira_issue_tracker.JQL_QUERY_FOUR", ""):
                                tracker = JiraIssueTracker()
                                tracker.boxes = []

                                with patch.object(tracker, "create_issue_box") as mock_create:
                                    tracker.create_issue_boxes()

                                    self.assertEqual(tracker.cols, 2)
                                    self.assertEqual(mock_create.call_count, 2)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    def test_theme_preference_loading(self, mock_get_key):
        """Test loading saved theme preference"""
        def get_key_side_effect(file, key):
            if key == "THEME_PREFERENCE":
                return "Ocean"
            elif key == "JIRA_SITE_URL":
                return "https://dummy-jira-url.com"
            return None

        mock_get_key.side_effect = get_key_side_effect

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                self.assertEqual(tracker.current_theme_index, 1)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    def test_cycle_theme(self, mock_get_key):
        """Test cycling through themes"""
        mock_get_key.return_value = "https://dummy-jira-url.com"

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                with patch("jira_tracker.jira_issue_tracker.set_key") as mock_set_key:
                    with patch("builtins.__import__", side_effect=ImportError("No module named 'issue_box'")):
                        tracker = JiraIssueTracker()
                        tracker.boxes = []
                        initial_index = tracker.current_theme_index

                        try:
                            tracker.cycle_theme(None)
                        except (ImportError, ModuleNotFoundError):
                            pass

                        self.assertEqual(tracker.current_theme_index, (initial_index + 1) % len(tracker.theme_names))
                        mock_set_key.assert_called_once()

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_success(self, mock_get_results, mock_get_key):
        """Test updating labels successfully"""
        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com",
            "JIRA_SERVER": "true"
        }.get(key)
        mock_get_results.return_value = 42

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()

                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                mock_box.show_loading.assert_called_once()
                mock_box.update_label.assert_called_once_with(42)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_request_exception(self, mock_get_results, mock_get_key):
        """Test handling RequestException during update"""
        from requests.exceptions import RequestException

        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com",
            "JIRA_SERVER": "true"
        }.get(key)
        mock_get_results.side_effect = RequestException("401 Unauthorized")

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()

                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                mock_box.show_loading.assert_called_once()
                mock_box.update_label_error.assert_called_once()
                error_msg = mock_box.update_label_error.call_args[0][0]
                self.assertIn("Authentication Failed", error_msg)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_403_error(self, mock_get_results, mock_get_key):
        """Test handling 403 error"""
        from requests.exceptions import RequestException

        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com",
            "JIRA_SERVER": "true"
        }.get(key)
        mock_get_results.side_effect = RequestException("403 Forbidden")

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                error_msg = mock_box.update_label_error.call_args[0][0]
                self.assertIn("Access Denied", error_msg)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_404_error(self, mock_get_results, mock_get_key):
        """Test handling 404 error"""
        from requests.exceptions import RequestException

        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com",
            "JIRA_SERVER": "true"
        }.get(key)
        mock_get_results.side_effect = RequestException("404 Not Found")

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                error_msg = mock_box.update_label_error.call_args[0][0]
                self.assertIn("Jira URL Not Found", error_msg)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_timeout_error(self, mock_get_results, mock_get_key):
        """Test handling timeout error"""
        from requests.exceptions import RequestException

        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com",
            "JIRA_SERVER": "true"
        }.get(key)
        mock_get_results.side_effect = RequestException("Timeout occurred")

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                error_msg = mock_box.update_label_error.call_args[0][0]
                self.assertIn("Request Timeout", error_msg)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_cloud_mode(self, mock_get_results, mock_get_key):
        """Test update labels in cloud mode (no JIRA_SERVER)"""
        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com"
        }.get(key)
        mock_get_results.return_value = 99

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                mock_box.show_loading.assert_called_once()
                mock_box.update_label.assert_called_once_with(99)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    @patch("jira_tracker.jira_issue_tracker.get_jql_query_results")
    def test_update_labels_cloud_mode_error(self, mock_get_results, mock_get_key):
        """Test error handling in cloud mode"""
        from requests.exceptions import RequestException

        mock_get_key.side_effect = lambda file, key: {
            "JIRA_SITE_URL": "https://dummy-jira-url.com"
        }.get(key)
        mock_get_results.side_effect = RequestException("Connection error")

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                mock_box = MagicMock()
                mock_box.jql_query = "project = TEST"
                tracker.boxes = [mock_box]

                tracker.update_labels(0)

                error_msg = mock_box.update_label_error.call_args[0][0]
                self.assertIn("Connection Error", error_msg)

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_create_user_settings_button(self, mock_get_key):
        """Test create_user_settings_button (deprecated method)"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                result = tracker.create_user_settings_button()
                self.assertIsNone(result)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    def test_toggle_mode(self, mock_get_key):
        """Test toggle_mode switches theme"""
        mock_get_key.return_value = "https://dummy-jira-url.com"

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                with patch("jira_tracker.jira_issue_tracker.MDApp") as mock_mdapp:
                    mock_app = MagicMock()
                    mock_app.theme_cls.theme_style = "Dark"
                    mock_mdapp.get_running_app.return_value = mock_app

                    tracker = JiraIssueTracker()
                    mock_box = MagicMock()
                    tracker.boxes = [mock_box]

                    tracker.toggle_mode(None)

                    self.assertEqual(mock_app.theme_cls.theme_style, "Light")
                    mock_box.update_ui_colors.assert_called_once_with("Light")

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_initialization_sets_jira_base_url(self, mock_get_key):
        """Test that initialization properly sets jira_base_url"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                self.assertEqual(tracker.jira_site_url, "https://dummy-jira-url.com")
                self.assertEqual(tracker.jira_base_url, "https://dummy-jira-url.com/issues/")

    @patch("jira_tracker.jira_issue_tracker.get_key")
    def test_initialization_dark_mode_default(self, mock_get_key):
        """Test that dark mode is enabled by default"""
        mock_get_key.return_value = "https://dummy-jira-url.com"

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                self.assertTrue(tracker.dark_mode)

    @patch("jira_tracker.jira_issue_tracker.get_key")
    def test_initialization_theme_names(self, mock_get_key):
        """Test that theme names list is properly initialized"""
        mock_get_key.return_value = "https://dummy-jira-url.com"

        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                tracker = JiraIssueTracker()
                self.assertEqual(len(tracker.theme_names), 5)
                self.assertIn("Default", tracker.theme_names)
                self.assertIn("Ocean", tracker.theme_names)

    @patch("jira_tracker.jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_toggle_mode_from_light_to_dark(self, mock_get_key):
        """Test toggling from Light to Dark mode"""
        with patch.object(JiraIssueTracker, "setup_ui"):
            with patch.object(JiraIssueTracker, "add_widget"):
                with patch("jira_tracker.jira_issue_tracker.MDApp") as mock_mdapp:
                    mock_app = MagicMock()
                    mock_app.theme_cls.theme_style = "Light"
                    mock_mdapp.get_running_app.return_value = mock_app

                    tracker = JiraIssueTracker()
                    mock_box = MagicMock()
                    tracker.boxes = [mock_box]

                    tracker.toggle_mode(None)

                    self.assertEqual(mock_app.theme_cls.theme_style, "Dark")


if __name__ == "__main__":
    unittest.main()
