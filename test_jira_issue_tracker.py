import unittest
from unittest.mock import patch, MagicMock
from jira_issue_tracker import JiraIssueTracker


class TestJiraIssueTracker(unittest.TestCase):

    @patch("jira_issue_tracker.get_key", return_value="https://dummy-jira-url.com")
    def test_initialization(self, mock_get_key):
        # Test initialization without creating Kivy window or app
        with patch("jira_issue_tracker.MDLabel") as mock_mdlabel:
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


if __name__ == "__main__":
    unittest.main()
