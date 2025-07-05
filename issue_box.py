import os
import urllib
import webbrowser

# Conditional imports for CI environment
if os.environ.get("CI") != "true":
    from kivymd.uix.label import MDLabel
    from kivymd.uix.card import MDCard
    from kivymd.uix.spinner import MDSpinner
    from kivymd.uix.tooltip import MDTooltip
    from kivymd.app import MDApp
    from kivy.utils import get_color_from_hex
else:
    # Mock classes for CI environment
    class MDLabel:
        def __init__(self, **kwargs):
            pass

    class MDCard:
        def __init__(self, **kwargs):
            pass

    class MDSpinner:
        def __init__(self, **kwargs):
            pass

    class MDTooltip:
        def __init__(self, **kwargs):
            pass

    class MDApp:
        @staticmethod
        def get_running_app():
            return None

    def get_color_from_hex(hex_color):
        return (0, 0, 0, 1)


# Define your text colors for dark and light themes
LIGHT_TEXT_COLOR = get_color_from_hex("ffffff")  # White text for dark backgrounds
DARK_TEXT_COLOR = get_color_from_hex("000000")  # Black text for light backgrounds


class IssueBox(MDCard):
    def __init__(self, title, jql_query, jira_base_url, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.jql_query = jql_query
        self.jira_base_url = jira_base_url
        self.focus_behavior = True
        self.ripple_behavior = True
        self.elevation = True
        self.jql_label = None
        self.title_label = None
        self.issue_label = None
        self.loading_spinner = None
        self.is_loading = False

        self.setup_ui()

    def setup_ui(self):
        """Initializes the user interface for the issue box."""
        self.size_hint = (0.5, None)  # Use half the width of the parent
        self.height = "160dp"  # Increased height to accommodate spinner
        self.padding = "12dp"  # Increased padding for better spacing
        self.orientation = "vertical"
        self.create_labels()
        self.create_loading_spinner()
        self.add_tooltips()

    def add_tooltips(self):
        """Add tooltips to explain functionality."""
        # Only add tooltips if app is running (avoid test issues)
        try:
            app = MDApp.get_running_app()
            if app:
                # Tooltip for the entire card explaining click functionality
                card_tooltip = MDTooltip(
                    tooltip_text="Click to view these issues in Jira", widget=self
                )

                # Tooltip for the JQL query
                jql_tooltip = MDTooltip(
                    tooltip_text="Click to open this query in Jira",
                    widget=self.jql_label,
                )
        except:
            pass  # Skip tooltips if app context not available

    def create_loading_spinner(self):
        """Creates a loading spinner for API calls."""
        self.loading_spinner = MDSpinner(
            size_hint=(None, None),
            size=("24dp", "24dp"),
            pos_hint={"center_x": 0.5},
            active=False,
        )

    def create_labels(self):
        """Creates and adds labels to the issue box."""
        self.title_label = MDLabel(
            text=self.title,
            font_style="Subtitle1",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height="48dp",
        )
        self.issue_label = MDLabel(
            text="Fetching data...",
            font_style="H6",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="48dp",
        )
        # Adjust label height dynamically based on query length
        query_lines = self.jql_query.count("\n") + 1
        label_height = max(24, query_lines * 24)  # Adjust 24dp per line
        self.jql_label = MDLabel(
            text=self.jql_query,
            font_style="Caption",
            halign="center",
            theme_text_color="Hint",
            size_hint_y=None,
            height=f"{label_height}dp",
        )
        self.jql_label.bind(on_touch_down=self.on_jql_label_click)
        self.add_widget(self.title_label)
        self.add_widget(self.issue_label)
        self.add_widget(self.jql_label)

    def show_loading(self):
        """Shows the loading spinner and updates the label."""
        if not self.is_loading:
            self.is_loading = True
            self.issue_label.text = "Loading..."
            self.add_widget(self.loading_spinner)
            self.loading_spinner.active = True

    def hide_loading(self):
        """Hides the loading spinner."""
        if self.is_loading:
            self.is_loading = False
            self.loading_spinner.active = False
            if self.loading_spinner in self.children:
                self.remove_widget(self.loading_spinner)

    def on_jql_label_click(self, instance, touch):
        """Handles click events on the JQL label."""
        if self.collide_point(*touch.pos):
            jira_url = f"{self.jira_base_url}?jql={urllib.parse.quote(self.jql_query)}"
            webbrowser.open(jira_url)
            print("User Clicked:", jira_url)

    def update_label(self, count):
        """Updates the issue count label."""
        self.hide_loading()  # Hide loading when data arrives
        self.issue_label.text = str(count)
        self.issue_label.theme_text_color = "Secondary"  # Reset to normal color

    def update_label_error(self, error_message):
        """Updates the label with an error message."""
        self.hide_loading()  # Hide loading when error occurs
        self.issue_label.text = error_message
        self.issue_label.theme_text_color = "Error"  # Show error in red

    # Inside IssueBox class
    def update_ui_colors(self, theme_style):
        app = MDApp.get_running_app()
        if theme_style == "Dark":
            self.md_bg_color = app.theme_cls.bg_dark
            text_color = LIGHT_TEXT_COLOR
        else:
            self.md_bg_color = app.theme_cls.bg_light
            text_color = DARK_TEXT_COLOR

        # Update the text color of all the labels
        self.issue_label.color = text_color
        self.title_label.color = text_color
        self.jql_label.color = text_color
