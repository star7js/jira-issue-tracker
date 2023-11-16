from dotenv import set_key
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class JiraConnectionSettingsPopup(Popup):
    """
    Popup for Jira Connection Settings.
    """

    def __init__(self, **kwargs):
        super(JiraConnectionSettingsPopup, self).__init__(**kwargs)
        self.title = "Jira Connection Settings"

        save_button = Button(text="Save and Close Program", on_press=self.save_settings)
        close_without_save_button = Button(text="Close without Saving", on_press=self.dismiss)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.jira_site_url = TextInput(hint_text="Jira Site URL\n ()")
        self.jira_api_key = TextInput(hint_text="Jira Personal Access Token", multiline=False)

        layout.add_widget(self.jira_site_url)
        layout.add_widget(self.jira_api_key)
        layout.add_widget(save_button)
        layout.add_widget(close_without_save_button)

        self.content = layout

    def save_settings(self, instance):
        """
        Save the settings to the .env file and close the application.
        """
        jira_api_key = self.jira_api_key.text.strip()
        jira_site_url = self.jira_site_url.text.rstrip("/")

        try:
            if jira_api_key:
                set_key('.env', 'JIRA_API_KEY', jira_api_key)
            if jira_site_url:
                set_key('.env', 'JIRA_SITE_URL', jira_site_url)
            # Consider adding user feedback here, e.g., a confirmation popup.
        except Exception as e:
            # Handle exceptions, potentially logging them or notifying the user.
            pass

        App.get_running_app().stop()


def open_settings_popup(instance):
    """
    Open the settings popup.
    """
    popup = JiraConnectionSettingsPopup()
    popup.open()
