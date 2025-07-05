import unittest
from unittest.mock import patch
from kivy.base import EventLoop
from kivymd.app import MDApp
from jira_issue_tracker import JiraIssueTracker


class TestApp(MDApp):
    def build(self):
        return JiraIssueTracker()


class TestJiraIssueTracker(unittest.TestCase):

    @patch('jira_issue_tracker.get_key', return_value='https://dummy-jira-url.com')
    def test_initialization(self, mock_get_key):
        # Start the Kivy event loop
        EventLoop.ensure_window()
        app = TestApp()
        jira_issue_tracker = app.build()

        # Perform your tests here
        self.assertIsNotNone(jira_issue_tracker.jira_site_url)
        self.assertIsNotNone(jira_issue_tracker.jira_base_url)

        # Stop the Kivy event loop
        app.stop()


if __name__ == '__main__':
    unittest.main()
