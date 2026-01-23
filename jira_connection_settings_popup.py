import os
from dotenv import load_dotenv, set_key, find_dotenv, get_key
from logging_config import get_logger

logger = get_logger(__name__)

# Conditional imports for CI environment
if os.environ.get("CI") != "true":
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.dialog import MDDialog
    from kivymd.app import MDApp
    from kivymd.uix.label import MDLabel
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.button import MDRaisedButton
else:
    # Mock classes for CI environment
    class MDTextField:
        def __init__(self, **kwargs):
            pass

    class MDDialog:
        def __init__(self, **kwargs):
            pass

    class MDApp:
        @staticmethod
        def get_running_app():
            return None

    class MDLabel:
        def __init__(self, **kwargs):
            pass

    class MDBoxLayout:
        def __init__(self, **kwargs):
            pass

    class MDRaisedButton:
        def __init__(self, **kwargs):
            pass


class JiraConnectionSettingsPopup(MDDialog):
    def __init__(self, **kwargs):
        # Load environment variables from .env file
        load_dotenv(find_dotenv())

        # Get current values from .env, if they exist
        current_jira_site_url = get_key(".env", "JIRA_SITE_URL") or "Jira Site URL"
        current_jira_email = get_key(".env", "JIRA_EMAIL") or ""
        current_jira_api_token = (
            get_key(".env", "JIRA_API_TOKEN") or "Jira Personal Access Token"
        )

        # Create labels
        jira_site_url_label = MDLabel(
            text="Jira Site URL", halign="center", size_hint_y=None, height="20dp"
        )

        jira_email_label = MDLabel(
            text="Email (Required for Cloud only)",
            halign="center",
            size_hint_y=None,
            height="20dp",
        )

        jira_api_key_label = MDLabel(
            text="API Token",
            halign="center",
            size_hint_y=None,
            height="20dp",
        )

        self.jira_site_url = MDTextField(
            hint_text="https://yourcompany.atlassian.net",
            text=(
                current_jira_site_url
                if current_jira_site_url != "Jira Site URL"
                else ""
            ),
            size_hint=(1, None),
            height="48dp",
            multiline=False,
            font_size="14sp",
        )

        self.jira_email = MDTextField(
            hint_text="your.email@company.com",
            text=current_jira_email,
            size_hint=(1, None),
            height="48dp",
            multiline=False,
            font_size="14sp",
        )

        self.jira_api_token = MDTextField(
            hint_text="Enter your API token",
            size_hint=(1, None),
            height="48dp",
            multiline=False,
            password=True,
            font_size="12sp",
        )

        # MDBoxLayout for content
        content = MDBoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            spacing=12,
            size_hint_y=None,
            height="300dp",  # Increased height for email field
        )

        # Add widgets to the layout
        content.add_widget(jira_site_url_label)
        content.add_widget(self.jira_site_url)
        content.add_widget(jira_email_label)
        content.add_widget(self.jira_email)
        content.add_widget(jira_api_key_label)
        content.add_widget(self.jira_api_token)

        save_button = MDRaisedButton(
            text="Save and Close Program", on_release=self.save_settings
        )
        close_without_save_button = MDRaisedButton(
            text="Close without Saving", on_release=lambda x: self.dismiss()
        )

        # Adjust the size_hint for more space
        super().__init__(
            type="custom",
            content_cls=content,
            buttons=[save_button, close_without_save_button],
            size_hint=(0.9, 0.8),
        )

        # Set the height for MDTextFields to None to allow for auto-sizing
        self.jira_site_url.height = "30dp"
        self.jira_email.height = "30dp"
        self.jira_api_token.height = "30dp"

    def save_settings(self, instance):
        jira_api_token = self.jira_api_token.text.strip()
        jira_site_url = self.jira_site_url.text.rstrip("/")
        jira_email = self.jira_email.text.strip()

        try:
            if jira_email:
                set_key(".env", "JIRA_EMAIL", jira_email)
            if jira_api_token:
                set_key(".env", "JIRA_API_TOKEN", jira_api_token)
            if jira_site_url:
                set_key(".env", "JIRA_SITE_URL", jira_site_url)
            self.dismiss()
            MDApp.get_running_app().stop()
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            self.dismiss()


def open_settings_popup(instance):
    popup = JiraConnectionSettingsPopup()
    popup.open()


class JiraQueryEditorPopup(MDDialog):
    def __init__(self, **kwargs):
        # Load current JQL queries
        load_dotenv(find_dotenv())

        query_one = get_key(".env", "JQL_QUERY_ONE") or ""
        query_two = get_key(".env", "JQL_QUERY_TWO") or ""
        query_three = get_key(".env", "JQL_QUERY_THREE") or ""
        query_four = get_key(".env", "JQL_QUERY_FOUR") or ""

        # Create text fields for each query
        self.query_one_field = MDTextField(
            text=query_one,
            hint_text="Query One JQL",
            multiline=True,
            size_hint=(1, None),
            height="80dp",
        )

        self.query_two_field = MDTextField(
            text=query_two,
            hint_text="Query Two JQL",
            multiline=True,
            size_hint=(1, None),
            height="80dp",
        )

        self.query_three_field = MDTextField(
            text=query_three,
            hint_text="Query Three JQL",
            multiline=True,
            size_hint=(1, None),
            height="80dp",
        )

        self.query_four_field = MDTextField(
            text=query_four,
            hint_text="Query Four JQL",
            multiline=True,
            size_hint=(1, None),
            height="80dp",
        )

        # Content layout
        content = MDBoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            spacing=12,
            size_hint_y=None,
            height="400dp",
        )

        content.add_widget(
            MDLabel(
                text="Edit JQL Queries",
                font_style="H6",
                size_hint_y=None,
                height="30dp",
            )
        )
        content.add_widget(self.query_one_field)
        content.add_widget(self.query_two_field)
        content.add_widget(self.query_three_field)
        content.add_widget(self.query_four_field)

        save_button = MDRaisedButton(
            text="Save and Restart", on_release=self.save_queries
        )
        close_button = MDRaisedButton(
            text="Cancel", on_release=lambda x: self.dismiss()
        )

        super().__init__(
            type="custom",
            content_cls=content,
            buttons=[save_button, close_button],
            size_hint=(0.9, None),
            height="550dp",
        )

    def save_queries(self, instance):
        try:
            set_key(".env", "JQL_QUERY_ONE", self.query_one_field.text.strip())
            set_key(".env", "JQL_QUERY_TWO", self.query_two_field.text.strip())
            set_key(".env", "JQL_QUERY_THREE", self.query_three_field.text.strip())
            set_key(".env", "JQL_QUERY_FOUR", self.query_four_field.text.strip())
            self.dismiss()
            MDApp.get_running_app().stop()
        except Exception as e:
            logger.error(f"Error saving queries: {e}")
            self.dismiss()


def open_query_editor(instance):
    popup = JiraQueryEditorPopup()
    popup.open()
