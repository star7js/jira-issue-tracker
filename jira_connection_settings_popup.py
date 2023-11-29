from dotenv import load_dotenv, set_key, find_dotenv
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
import os


class JiraConnectionSettingsPopup(MDDialog):
    def __init__(self, **kwargs):
        # Load environment variables from .env file
        load_dotenv(find_dotenv())

        # Get current values from .env, if they exist
        current_jira_site_url = os.getenv('JIRA_SITE_URL', 'Jira Site URL')
        current_jira_api_token= os.getenv('JIRA_API_TOKEN', 'Jira Personal Access Token')

        # Create labels
        jira_site_url_label = MDLabel(
            text="Jira Site URL",
            halign="center",
            size_hint_y=None,
            height="20dp"
        )

        jira_api_key_label = MDLabel(
            text="Jira Personal Access Token",
            halign="center",
            size_hint_y=None,
            height="20dp"
        )

        self.jira_site_url = MDTextField(
            hint_text=current_jira_site_url,
            size_hint=(1, None),
            height="48dp",
            multiline=False
        )

        self.jira_api_token = MDTextField(
            hint_text=current_jira_api_token,
            size_hint=(1, None),
            height="48dp",
            multiline=False
        )

        # MDBoxLayout for content
        content = MDBoxLayout(
            orientation='vertical',
            padding=[10, 20, 10, 20],
            spacing=15,
            size_hint_y=None,
            height="200dp"  # Adjusted height to accommodate labels
        )

        # Add widgets to the layout
        content.add_widget(jira_site_url_label)
        content.add_widget(self.jira_site_url)
        content.add_widget(jira_api_key_label)
        content.add_widget(self.jira_api_token)

        save_button = MDRaisedButton(
            text="Save and Close Program",
            on_release=self.save_settings
        )
        close_without_save_button = MDRaisedButton(
            text="Close without Saving",
            on_release=lambda x: self.dismiss()
        )

        # Adjust the size_hint for more space
        super().__init__(
            type="custom",
            content_cls=content,
            buttons=[save_button, close_without_save_button],
            size_hint=(0.9, 0.8),
        )

        # Set the height for MDTextFields to None to allow for auto-sizing
        self.jira_site_url.height = '30dp'
        self.jira_api_token.height = '30dp'

    def save_settings(self, instance):
        jira_api_token = self.jira_api_token.text.strip()
        jira_site_url = self.jira_site_url.text.rstrip("/")

        try:
            if jira_api_token:
                set_key('.env', 'JIRA_API_TOKEN', jira_api_token)
            if jira_site_url:
                set_key('.env', 'JIRA_SITE_URL', jira_site_url)
            self.dismiss()
            MDApp.get_running_app().stop()
        except Exception as e:
            # Handle exceptions, potentially logging them or notifying the user
            print(e)
            self.dismiss()


def open_settings_popup(instance):
    popup = JiraConnectionSettingsPopup()
    popup.open()
