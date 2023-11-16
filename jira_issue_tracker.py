from dotenv import get_key
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from requests.exceptions import RequestException

import config
from api import get_jql_query_results
from issue_box import IssueBox


class JiraIssueTracker(GridLayout):
    # TODO: Fix Service Management Projects, is it JSON differences or is it user roleS?
    # TODO: Let the user select JQL Queries
    # TODO: Click to visit hint on the JQL box
    # TODO: Changes to the appearance of the box if desired
    # TODO: Complicated filters might need to be referenced by their number,
    # or else we need to format the data (regex to change "" to '', others?)

    JQL_QUERIES = [
        ("One", "assignee = currentUser()"),
        ("Two", "updated >= -1d order by updated DESC"),
        ("Three", "project = DEV and updated >= -14d"),
        ("Four", "project = SABR")
    ]

    jira_site_url = get_key('.env', 'JIRA_SITE_URL')
    jira_base_url = f"{jira_site_url}/issues/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boxes = None
        self.mode_button = None
        self.jira_base_url = self.jira_base_url
        self.dark_mode = True
        self.setup_ui()

    def setup_ui(self):
        self.cols = 2
        self.spacing = 10
        self.padding = 10
        self.create_issue_boxes()
        Clock.schedule_interval(self.update_labels, config.SIXTY_MINUTES)
        self.update_labels(0)
        self.create_mode_toggle_button()
        self.create_user_settings_button()

    def create_mode_toggle_button(self):
        self.mode_button = Button(text="Toggle Light/Dark Mode", size_hint_y=None, height=50)
        self.mode_button.bind(on_press=self.toggle_mode)
        self.add_widget(self.mode_button)

    def create_user_settings_button(self):
        self.mode_button = Button(text="User Settings", size_hint_y=None, height=50)
        self.mode_button.bind(on_press=open_settings_popup)
        self.add_widget(self.mode_button)

    def toggle_mode(self, instance):
        self.dark_mode = not self.dark_mode
        for box in self.boxes:
            box.update_ui_colors(self.dark_mode)

    def create_issue_boxes(self):
        self.boxes = [IssueBox(title, query, self.jira_base_url, self.dark_mode) for title, query in self.JQL_QUERIES]
        for box in self.boxes:
            self.add_widget(box)

    def update_labels(self, dt):
        for box in self.boxes:
            try:
                count = get_jql_query_results(self.jira_base_url, box.jql_query)
                box.update_label(count)
            except RequestException:
                box.update_label("Error fetching data")
