import kivy
from dotenv import get_key
from kivy.app import App

from jira_connection_settings_popup import JiraConnectionSettingsPopup
from jira_issue_tracker import JiraIssueTracker

kivy.require('2.1.0')


class JiraTrackerApp(App):

    def build(self):
        # if there are not environment variables set in a .env file, then we need the user to put them in
        if not (get_key('.env', 'JIRA_API_KEY') and get_key('.env', 'JIRA_SITE_URL')):
            return JiraConnectionSettingsPopup()

        else:
            # the variables were set so we can attempt to use them to get information from Jira Server
            return JiraIssueTracker()


if __name__ == '__main__':
    JiraTrackerApp().run()
