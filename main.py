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
    title = "Jira Tracker"  # Clean title without "App" suffix
    icon = "icon.png"  # Custom app icon

    def build(self):
        # Configure window appearance
        from kivy.core.window import Window
        from kivy.utils import get_color_from_hex

        # Set window size (optimal proportions)
        Window.size = (620, 540)
        Window.minimum_width = 580
        Window.minimum_height = 540

        # Set window background to dark (RGBA format)
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        # Set modern dark theme with vibrant colors (skip in CI/test mode)
        if hasattr(self, "theme_cls"):
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "DeepPurple"
            self.theme_cls.accent_palette = "Cyan"

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
