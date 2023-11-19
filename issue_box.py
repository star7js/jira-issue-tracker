import urllib
import webbrowser
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex

# Define your text colors for dark and light themes
LIGHT_TEXT_COLOR = get_color_from_hex('ffffff')  # White text for dark backgrounds
DARK_TEXT_COLOR = get_color_from_hex('000000')  # Black text for light backgrounds


class IssueBox(MDCard):
    def __init__(self, title, jql_query, jira_base_url, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.jql_query = jql_query
        self.jira_base_url = jira_base_url

        self.jql_label = None
        self.title_label = None
        self.issue_label = None

        self.setup_ui()

    def setup_ui(self):
        """Initializes the user interface for the issue box."""
        self.size_hint = (0.5, None)  # Use half the width of the parent
        self.height = "240dp"  # Set a height that allows for padding and readability
        self.padding = "8dp"  # Add some padding inside the card
        self.create_labels()

    def create_labels(self):
        """Creates and adds labels to the issue box."""
        self.issue_label = MDLabel(
            text="Fetching data...",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="48dp",
        )
        self.title_label = MDLabel(
            text=self.title,
            font_style="Subtitle1",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height="36dp",
        )
        self.jql_label = MDLabel(
            text=self.jql_query,
            font_style="Caption",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height="24dp",
        )
        self.jql_label.bind(on_touch_down=self.on_jql_label_click)
        self.add_widget(self.title_label)
        self.add_widget(self.issue_label)
        self.add_widget(self.jql_label)

    def on_jql_label_click(self, instance, touch):
        """Handles click events on the JQL label."""
        if self.collide_point(*touch.pos):
            jira_url = f"{self.jira_base_url}?jql={urllib.parse.quote(self.jql_query)}"
            webbrowser.open(jira_url)
            print("User Clicked:", jira_url)

    def update_label(self, count):
        """Updates the issue count label."""
        self.issue_label.text = str(count)

    # Inside IssueBox class
    def update_ui_colors(self, theme_style):
        app = MDApp.get_running_app()
        if theme_style == 'Dark':
            self.md_bg_color = app.theme_cls.bg_dark
            text_color = LIGHT_TEXT_COLOR
        else:
            self.md_bg_color = app.theme_cls.bg_light
            text_color = DARK_TEXT_COLOR

        # Update the text color of all the labels
        self.issue_label.color = text_color
        self.title_label.color = text_color
        self.jql_label.color = text_color
