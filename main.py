import os
from dotenv import get_key
from env_validator import validate_env_file, validate_jira_url
from logging_config import get_logger

logger = get_logger(__name__)

# Conditional imports for CI environment
if os.environ.get("CI") != "true":
    from kivymd.app import MDApp
    from jira_issue_tracker import JiraIssueTracker
    from jira_connection_settings_popup import JiraConnectionSettingsPopup
else:
    from ci_mocks import MDApp, JiraIssueTracker, JiraConnectionSettingsPopup


class JiraTrackerApp(MDApp):
    def build(self):
        # Validate .env file exists and has required variables
        is_valid, missing_vars = validate_env_file()

        if not is_valid:
            logger.warning(f"Environment validation failed: {missing_vars}")
            return JiraConnectionSettingsPopup()

        # Validate Jira URL format
        jira_site_url = get_key(".env", "JIRA_SITE_URL")
        if not validate_jira_url(jira_site_url):
            logger.warning(f"Invalid Jira URL format: {jira_site_url}")
            return JiraConnectionSettingsPopup()

        # If environment variables are set and valid, show the main tracker
        return JiraIssueTracker()


def main():
    JiraTrackerApp().run()


if __name__ == "__main__":
    main()
