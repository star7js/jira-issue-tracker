from dotenv import get_key
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from requests.exceptions import RequestException
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp

from api import (get_jql_query_results, DEFAULT_API_REQUEST_INTERVAL,
                 JQL_QUERY_ONE, JQL_QUERY_TWO, JQL_QUERY_THREE,
                 JQL_QUERY_FOUR)
from issue_box import IssueBox
from jira_connection_settings_popup import open_settings_popup


class JiraIssueTracker(GridLayout):
    # TODO: Fix Service Management Projects, is it JSON differences or is it user roleS? TODO: Let the user select
    #  TODO: Click to visit hint on the JQL box TODO: Changes to the appearance of the box if desired
    #   TODO: Complicated filters might need to be referenced by their number, or else we need to format the data (
    #    regex to change "" to '', others?)

    jira_site_url = get_key('.env', 'JIRA_SITE_URL')
    jira_base_url = f"{jira_site_url}/issues/"

    def create_issue_box(self, title, query):
        box = IssueBox(title, query, self.jira_base_url)
        self.add_widget(box)
        self.boxes.append(box)

    def create_issue_boxes(self):
        # Create a dictionary of query titles and their respective JQL queries
        jql_queries = {
            "Query One": JQL_QUERY_ONE,
            "Query Two": JQL_QUERY_TWO,
            "Query Three": JQL_QUERY_THREE,
            "Query Four": JQL_QUERY_FOUR
        }

        # Iterate through the dictionary and create a box for each non-empty query
        for title, query in jql_queries.items():
            if query:  # Only create a box if the query is defined (not None or empty)
                self.create_issue_box(title, query)

    def toggle_mode(self, instance):
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = 'Dark' if app.theme_cls.theme_style == 'Light' else 'Light'
        self.update_ui_for_theme(app.theme_cls.theme_style)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boxes = []  # Initialize self.boxes as an empty list
        self.mode_button = None
        self.jira_base_url = self.jira_base_url
        self.dark_mode = True
        self.setup_ui()

    def setup_ui(self):
        self.cols = 2
        self.spacing = 10
        self.padding = 10
        self.create_issue_boxes()
        Clock.schedule_interval(self.update_labels, DEFAULT_API_REQUEST_INTERVAL)
        self.update_labels(0)
        self.create_mode_toggle_button()
        self.create_user_settings_button()

    def create_mode_toggle_button(self):
        self.mode_button = MDRaisedButton(
            text="Toggle Light/Dark Mode",
            size_hint=(.5, None),
            height=50,
            pos_hint={'center_x': 0.5}
        )
        self.mode_button.bind(on_press=self.toggle_mode)
        self.add_widget(self.mode_button)

    def create_user_settings_button(self):
        self.user_settings_button = MDRaisedButton(
            text="User Settings",
            size_hint=(.5, None),
            height=50,
            pos_hint={'center_x': 0.5}
        )
        self.user_settings_button.bind(on_press=open_settings_popup)
        self.add_widget(self.user_settings_button)

    def toggle_mode(self, instance):
        app = MDApp.get_running_app()
        new_theme_style = 'Dark' if app.theme_cls.theme_style == 'Light' else 'Light'
        app.theme_cls.theme_style = new_theme_style
        for box in self.boxes:
            box.update_ui_colors(new_theme_style)  # Pass the new_theme_style variable, not the property

    def update_labels(self, dt):
        for box in self.boxes:
            try:
                count = get_jql_query_results(box.jql_query)  # Only pass the JQL query
                box.update_label(count)
            except RequestException:
                box.update_label("Error fetching data")
