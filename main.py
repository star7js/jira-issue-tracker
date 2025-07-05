import os
from dotenv import get_key

# Conditional imports for CI environment
if os.environ.get("CI") != "true":
    from kivymd.app import MDApp
    from jira_issue_tracker import JiraIssueTracker
    from jira_connection_settings_popup import JiraConnectionSettingsPopup
else:
    # Mock classes for CI environment
    class MDApp:
        def __init__(self):
            pass

        def run(self):
            pass

    class JiraIssueTracker:
        def __init__(self):
            pass

    class JiraConnectionSettingsPopup:
        def __init__(self):
            pass


class JiraTrackerApp(MDApp):
    def build(self):
        # Check if environment variables are set
        jira_site_url = get_key(".env", "JIRA_SITE_URL")

        if not jira_site_url:
            # If environment variables are not set, show settings popup
            return JiraConnectionSettingsPopup()
        else:
            # If environment variables are set, show the main tracker
            return JiraIssueTracker()


def main():
    JiraTrackerApp().run()


if __name__ == "__main__":
    main()
