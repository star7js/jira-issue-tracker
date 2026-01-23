import os
from dotenv import get_key, set_key
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from requests.exceptions import RequestException

# Conditional imports for CI environment
if os.environ.get("CI") != "true":
    from kivymd.uix.button import MDRaisedButton, MDIconButton
    from kivymd.uix.tooltip import MDTooltip
    from kivymd.app import MDApp
    from kivymd.uix.label import MDLabel
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.floatlayout import FloatLayout
else:
    from ci_mocks import MDRaisedButton, MDTooltip, MDApp, MDLabel


from api import (
    get_jql_query_results,
    DEFAULT_API_REQUEST_INTERVAL,
    JQL_QUERY_ONE,
    JQL_QUERY_TWO,
    JQL_QUERY_THREE,
    JQL_QUERY_FOUR,
)
from issue_box import IssueBox
from jira_connection_settings_popup import open_settings_popup, open_query_editor

# UI Constants - Dashboard widget styling
ERROR_COLOR_RED = (1, 0, 0, 1)
GRID_SPACING = 12  # Tight, clean spacing
GRID_PADDING = 20  # Balanced edge padding


class JiraIssueTracker(GridLayout):
    """Main Jira Issue Tracker widget that displays issue counts in a grid layout."""

    def create_issue_box(self, title, query):
        box = IssueBox(title, query, self.jira_base_url, theme_name=self.theme_names[self.current_theme_index])
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
        self.theme_names = ["Default", "Ocean", "Sunset", "Forest", "Nord"]

        # Load saved theme preference
        saved_theme = get_key(".env", "THEME_PREFERENCE") or "Default"
        self.current_theme_index = self.theme_names.index(saved_theme) if saved_theme in self.theme_names else 0

        self.jira_site_url = get_key(".env", "JIRA_SITE_URL")
        self.jira_base_url = (
            f"{self.jira_site_url}/issues/" if self.jira_site_url else None
        )
        self.dark_mode = True
        if not self.jira_site_url:
            error_label = MDLabel(
                text="⚠️  Error: Jira Site URL is not set. Please configure your connection in settings.",
                color=ERROR_COLOR_RED,
                halign="center",
                theme_text_color="Error",
                font_style="Body1",
            )
            self.add_widget(error_label)
        else:
            self.setup_ui()

    def setup_ui(self):
        from kivy.utils import get_color_from_hex
        self.cols = 2
        self.spacing = GRID_SPACING
        self.padding = GRID_PADDING

        # Set dark background for modern look
        app = MDApp.get_running_app()
        self.md_bg_color = get_color_from_hex("1a1a1a")

        self.create_issue_boxes()
        Clock.schedule_interval(self.update_labels, DEFAULT_API_REQUEST_INTERVAL)
        self.update_labels(0)
        self.create_mode_toggle_button()
        self.create_user_settings_button()

    def create_mode_toggle_button(self):
        """Create small icon buttons for app controls."""
        if os.environ.get("CI") == "true":
            return

        # No spacer needed - tight layout

        # Create a horizontal box layout for icon buttons
        button_box = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height="40dp",
            spacing="16dp",
            padding=["12dp", "0dp", "12dp", "4dp"],
        )

        # Theme switcher button
        theme_btn = MDIconButton(
            icon="palette",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.6),
            pos_hint={"center_y": 0.5},
        )
        theme_btn.bind(on_press=self.cycle_theme)

        # Query editor button
        query_btn = MDIconButton(
            icon="pencil",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.6),
            pos_hint={"center_y": 0.5},
        )
        query_btn.bind(on_press=open_query_editor)

        # Refresh icon button
        refresh_btn = MDIconButton(
            icon="refresh",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.6),
            pos_hint={"center_y": 0.5},
        )
        refresh_btn.bind(on_press=lambda x: self.update_labels(0))

        # Settings icon button
        settings_btn = MDIconButton(
            icon="cog",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.6),
            pos_hint={"center_y": 0.5},
        )
        settings_btn.bind(on_press=open_settings_popup)

        # Add buttons to the box
        button_box.add_widget(theme_btn)
        button_box.add_widget(query_btn)
        button_box.add_widget(refresh_btn)
        button_box.add_widget(settings_btn)

        # Add empty left column spacer to push button_box to right column
        from kivy.uix.widget import Widget
        self.add_widget(Widget())
        self.add_widget(button_box)

    def create_user_settings_button(self):
        """Deprecated - settings now in icon button."""
        pass

    def cycle_theme(self, instance):
        """Cycle through available themes."""
        # Move to next theme
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_names)
        new_theme_name = self.theme_names[self.current_theme_index]

        # Save theme preference to .env
        try:
            set_key(".env", "THEME_PREFERENCE", new_theme_name)
        except:
            pass  # Silently fail if can't save

        # Update all boxes with new theme
        from issue_box import THEMES
        for box in self.boxes:
            if box.title in THEMES[new_theme_name]:
                box.gradient_colors = THEMES[new_theme_name][box.title]
                box.md_bg_color = box.gradient_colors["start"]
                # Update icon if it changed
                if hasattr(box, 'icon_label') and box.icon_label:
                    box.icon_label.icon = box.gradient_colors["icon"]

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
