import unittest
from kivy.base import EventLoop
from kivymd.app import MDApp
from jira_issue_tracker import JiraIssueTracker


class TestApp(MDApp):
    def build(self):
        return JiraIssueTracker()


class TestJiraIssueTracker(unittest.TestCase):

    def test_initialization(self):
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
