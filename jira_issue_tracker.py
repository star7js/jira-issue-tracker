from dotenv import get_key
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from requests.exceptions import RequestException
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from api import (
    get_jql_query_results,
    DEFAULT_API_REQUEST_INTERVAL,
    JQL_QUERY_ONE,
    JQL_QUERY_TWO,
    JQL_QUERY_THREE,
    JQL_QUERY_FOUR,
)
from issue_box import IssueBox
from jira_connection_settings_popup import open_settings_popup


class JiraIssueTracker(GridLayout):
    # TODO: Fix Service Management Projects, is it JSON differences or is it user roleS? TODO: Let the user select
    #  TODO: Click to visit hint on the JQL box TODO: Changes to the appearance of the box if desired
    #   TODO: Complicated filters might need to be referenced by their number, or else we need to format the data (
    #    regex to change "" to '', others?)

    def create_issue_box(self, title, query):
        box = IssueBox(title, query, self.jira_base_url)
        self.add_widget(box)
        self.boxes.append(box)

    def create_empty_box(self):
        empty_box = IssueBox(title="", jql_query="", jira_base_url=self.jira_base_url)
        empty_box.disabled = True  # Optionally disable interaction
        self.add_widget(empty_box)

    def create_issue_boxes(self):
        # Dictionary of query titles and their respective JQL queries
        jql_queries = {
            "Query One": JQL_QUERY_ONE,
            "Query Two": JQL_QUERY_TWO,
            "Query Three": JQL_QUERY_THREE,
            "Query Four": JQL_QUERY_FOUR,
        }

        # Filter out empty queries and count them
        active_queries = {k: v for k, v in jql_queries.items() if v}
        query_count = len(active_queries)

        # Decide on the number of columns based on the number of active queries
        self.cols = 2 if query_count > 1 else 1

        # Create a box for each active query
        for title, query in active_queries.items():
            self.create_issue_box(title, query)

        # If the number of queries is less than four, fill in the empty spaces
        # for _ in range(6 - query_count):
        # self.create_empty_box()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boxes = []  # Initialize self.boxes as an empty list
        self.mode_button = None
        self.jira_site_url = get_key(".env", "JIRA_SITE_URL")
        self.jira_base_url = (
            f"{self.jira_site_url}/issues/" if self.jira_site_url else None
        )
        self.dark_mode = True
        if not self.jira_site_url:
            error_label = MDLabel(
                text="⚠️  Error: Jira Site URL is not set. Please configure your connection in settings.",
                color=(1, 0, 0, 1),
                halign="center",
                theme_text_color="Error",
                font_style="Body1",
            )
            self.add_widget(error_label)
        else:
            self.setup_ui()

    def setup_ui(self):
        self.cols = 2
        self.spacing = 20  # Increased from 10 for better separation
        self.padding = 20  # Increased from 10 for better margins
        self.create_issue_boxes()
        Clock.schedule_interval(self.update_labels, DEFAULT_API_REQUEST_INTERVAL)
        self.update_labels(0)
        self.create_mode_toggle_button()
        self.create_user_settings_button()

    def create_mode_toggle_button(self):
        # Add a separator label before buttons
        separator = MDLabel(
            text="", size_hint_y=None, height="20dp", theme_text_color="Hint"
        )
        self.add_widget(separator)

        self.mode_button = MDRaisedButton(
            text="Toggle Light/Dark Mode",
            size_hint=(0.5, None),
            height=50,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.2, 0.6, 1, 1),  # Blue color for better visibility
        )
        self.mode_button.bind(on_press=self.toggle_mode)

        # Add tooltip to mode button (only if app is running)
        try:
            app = MDApp.get_running_app()
            if app:
                tooltip = MDTooltip(
                    tooltip_text="Switch between light and dark themes for better visibility",
                    widget=self.mode_button,
                )
        except:
            pass  # Skip tooltip if app context not available

        self.add_widget(self.mode_button)

    def create_user_settings_button(self):
        self.user_settings_button = MDRaisedButton(
            text="User Settings",
            size_hint=(0.5, None),
            height=50,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.3, 0.7, 0.3, 1),  # Green color for settings
        )
        self.user_settings_button.bind(on_press=open_settings_popup)

        # Add tooltip to settings button (only if app is running)
        try:
            app = MDApp.get_running_app()
            if app:
                tooltip = MDTooltip(
                    tooltip_text="Configure Jira connection settings and credentials",
                    widget=self.user_settings_button,
                )
        except:
            pass  # Skip tooltip if app context not available

        self.add_widget(self.user_settings_button)

    def toggle_mode(self, instance):
        app = MDApp.get_running_app()
        new_theme_style = "Dark" if app.theme_cls.theme_style == "Light" else "Light"
        app.theme_cls.theme_style = new_theme_style
        for box in self.boxes:
            box.update_ui_colors(
                new_theme_style
            )  # Pass the new_theme_style variable, not the property

    def update_labels(self, dt):
        for box in self.boxes:
            box.show_loading()  # Show loading indicator
            if get_key(".env", "JIRA_SERVER"):
                try:
                    count = get_jql_query_results(
                        box.jql_query
                    )  # Only pass the JQL query
                    box.update_label(count)
                except RequestException as e:
                    error_msg = "Connection Error"
                    if "401" in str(e):
                        error_msg = "Authentication Failed - Check credentials"
                    elif "403" in str(e):
                        error_msg = "Access Denied - Check permissions"
                    elif "404" in str(e):
                        error_msg = "Jira URL Not Found - Check configuration"
                    elif "timeout" in str(e).lower():
                        error_msg = "Request Timeout - Check network connection"
                    box.update_label_error(error_msg)
            else:
                try:
                    count = get_jql_query_results(
                        box.jql_query
                    )  # Only pass the JQL query
                    box.update_label(count)
                except RequestException as e:
                    error_msg = "Connection Error"
                    if "401" in str(e):
                        error_msg = "Authentication Failed - Check credentials"
                    elif "403" in str(e):
                        error_msg = "Access Denied - Check permissions"
                    elif "404" in str(e):
                        error_msg = "Jira URL Not Found - Check configuration"
                    elif "timeout" in str(e).lower():
                        error_msg = "Request Timeout - Check network connection"
                    box.update_label_error(error_msg)
