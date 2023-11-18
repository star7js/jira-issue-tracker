from dotenv import set_key
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton


class JiraConnectionSettingsPopup(MDDialog):
    def __init__(self, **kwargs):
        self.jira_site_url = MDTextField(
            hint_text="Jira Site URL",
            size_hint=(1, None),  # Occupy the full width of the layout, height is None
            height="48dp",  # Minimum height
            multiline=False
        )

        self.jira_api_key = MDTextField(
            hint_text="Jira Personal Access Token",
            size_hint=(1, None),  # Occupy the full width of the layout, height is None
            height="48dp",  # Minimum height
            multiline=False
        )

        content = MDBoxLayout(
            orientation='vertical',
            padding=[10, 20, 10, 20],
            spacing=15,
            size_hint_y=None,  # Disable height scaling relative to the parent
            height="150dp"  # Set a fixed height of 300dp for the content box
        )

        content.add_widget(self.jira_site_url)
        content.add_widget(self.jira_api_key)

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
        self.jira_api_key.height = '30dp'

    def save_settings(self, instance):
        jira_api_key = self.jira_api_key.text.strip()
        jira_site_url = self.jira_site_url.text.rstrip("/")

        try:
            if jira_api_key:
                set_key('.env', 'JIRA_API_KEY', jira_api_key)
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
