import urllib
import webbrowser

from kivy.graphics import Rectangle, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

import config


class IssueBox(FloatLayout):
    def __init__(self, title, jql_query, jira_base_url, dark_mode=True, **kwargs):
        super().__init__(**kwargs)
        self.jql_label = None
        self.title_label = None
        self.issue_label = None
        self.rect = None
        self.jira_base_url = None
        self.jql_query = None
        self.title = None
        self.dark_mode = dark_mode
        self.setup_ui(title, jql_query, jira_base_url)

    def setup_ui(self, title, jql_query, jira_base_url):
        self.size = (200, 200)  # this is the square size of the JQL issue box
        self.size_hint = (None, None)
        self.pos_hint = {"center_x": 0.5}
        self.title = title
        self.jql_query = jql_query
        self.jira_base_url = jira_base_url

        self.update_ui_colors()
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.create_labels()

    def update_ui_colors(self, dark_mode=None):
        """Update UI colors based on the mode."""
        if dark_mode is None:
            dark_mode = self.dark_mode

        with self.canvas.before:
            if dark_mode:
                Color(*config.DARK_MODE_BACKGROUND_COLOR)
            else:
                Color(*config.LIGHT_MODE_BACKGROUND_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def create_labels(self):
        text_color = (1, 1, 1, 1) if self.dark_mode else (0, 0, 0, 1)
        self.issue_label = self.create_label("Fetching data...", 80, {"center_x": 0.5, "center_y": 0.5}, text_color)
        self.title_label = self.create_label(self.title, 12, {"top": 1.0, "center_x": 0.5}, text_color)
        self.jql_label = self.create_label(self.jql_query, 11, {"top": 0.9, "center_x": 0.5}, text_color)
        self.jql_label.bind(on_touch_down=self.on_jql_label_click)
        self.add_widget(self.issue_label)
        self.add_widget(self.title_label)
        self.add_widget(self.jql_label)

    @staticmethod
    def create_label(text, font_size, pos_hint, color=(1, 1, 1, 1)):
        return Label(
            text=text,
            font_size=font_size,
            color=color,
            size_hint_y=None,
            height=30,
            pos_hint=pos_hint,
            max_lines=1
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_label(self, count):
        self.issue_label.text = f"{count}"

    def on_jql_label_click(self, instance, touch):
        if self.collide_point(*touch.pos):
            jira_url = f"{self.jira_base_url}?jql={urllib.parse.quote(self.jql_query)}"
            webbrowser.open(jira_url)
            print("User Clicked:", jira_url)
