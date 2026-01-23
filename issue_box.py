import os
import urllib
import webbrowser

# Conditional imports for CI environment
if os.environ.get("CI") != "true":
    from kivymd.uix.label import MDLabel, MDIcon
    from kivymd.uix.card import MDCard
    from kivymd.uix.spinner import MDSpinner
    from kivymd.uix.tooltip import MDTooltip
    from kivymd.app import MDApp
    from kivy.utils import get_color_from_hex
    from kivy.graphics import Color, RoundedRectangle
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.widget import Widget
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

# Preset theme collections
THEMES = {
    "Default": {
        "Query One": {"start": get_color_from_hex("667eea"), "end": get_color_from_hex("764ba2"), "icon": "account-circle"},
        "Query Two": {"start": get_color_from_hex("f093fb"), "end": get_color_from_hex("f5576c"), "icon": "file-document"},
        "Query Three": {"start": get_color_from_hex("4facfe"), "end": get_color_from_hex("00f2fe"), "icon": "calendar-clock"},
        "Query Four": {"start": get_color_from_hex("43e97b"), "end": get_color_from_hex("38f9d7"), "icon": "alert-circle"}
    },
    "Ocean": {
        "Query One": {"start": get_color_from_hex("2E3192"), "end": get_color_from_hex("1BFFFF"), "icon": "account-circle"},
        "Query Two": {"start": get_color_from_hex("00d2ff"), "end": get_color_from_hex("3a7bd5"), "icon": "file-document"},
        "Query Three": {"start": get_color_from_hex("108dc7"), "end": get_color_from_hex("ef8e38"), "icon": "calendar-clock"},
        "Query Four": {"start": get_color_from_hex("134E5E"), "end": get_color_from_hex("71B280"), "icon": "alert-circle"}
    },
    "Sunset": {
        "Query One": {"start": get_color_from_hex("FF512F"), "end": get_color_from_hex("DD2476"), "icon": "account-circle"},
        "Query Two": {"start": get_color_from_hex("FF6B6B"), "end": get_color_from_hex("FFE66D"), "icon": "file-document"},
        "Query Three": {"start": get_color_from_hex("ee9ca7"), "end": get_color_from_hex("ffdde1"), "icon": "calendar-clock"},
        "Query Four": {"start": get_color_from_hex("fc4a1a"), "end": get_color_from_hex("f7b733"), "icon": "alert-circle"}
    },
    "Forest": {
        "Query One": {"start": get_color_from_hex("134E5E"), "end": get_color_from_hex("71B280"), "icon": "account-circle"},
        "Query Two": {"start": get_color_from_hex("56ab2f"), "end": get_color_from_hex("a8e063"), "icon": "file-document"},
        "Query Three": {"start": get_color_from_hex("2C5F2D"), "end": get_color_from_hex("97BC62"), "icon": "calendar-clock"},
        "Query Four": {"start": get_color_from_hex("0F2027"), "end": get_color_from_hex("2C5364"), "icon": "alert-circle"}
    },
    "Nord": {
        "Query One": {"start": get_color_from_hex("5E81AC"), "end": get_color_from_hex("81A1C1"), "icon": "account-circle"},
        "Query Two": {"start": get_color_from_hex("88C0D0"), "end": get_color_from_hex("8FBCBB"), "icon": "file-document"},
        "Query Three": {"start": get_color_from_hex("B48EAD"), "end": get_color_from_hex("A3BE8C"), "icon": "calendar-clock"},
        "Query Four": {"start": get_color_from_hex("BF616A"), "end": get_color_from_hex("D08770"), "icon": "alert-circle"}
    }
}

# Default theme
CURRENT_THEME = "Default"
TILE_GRADIENTS = THEMES[CURRENT_THEME]


class IssueBox(MDCard):
    def __init__(self, title, jql_query, jira_base_url, theme_name="Default", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.jql_query = jql_query
        self.jira_base_url = jira_base_url
        self.focus_behavior = True
        self.ripple_behavior = True
        self.elevation = 8
        self.jql_label = None
        self.title_label = None
        self.issue_label = None
        self.icon_label = None
        self.loading_spinner = None
        self.is_loading = False

        # Use the specified theme
        theme_colors = THEMES.get(theme_name, THEMES["Default"])
        self.gradient_colors = theme_colors.get(title, theme_colors["Query One"])

        self.setup_ui()

    def setup_ui(self):
        """Initializes the user interface for the issue box."""
        self.size_hint_x = 1  # Equal width for all tiles in grid
        self.size_hint_y = None
        self.height = "210dp"  # Perfect height for content
        self.padding = "24dp"  # Generous padding
        self.spacing = "6dp"  # Tight vertical spacing
        self.orientation = "vertical"
        self.radius = [18, 18, 18, 18]  # Smooth rounded corners

        # Apply gradient background
        self.md_bg_color = self.gradient_colors["start"]

        self.create_labels()
        self.create_loading_spinner()
        self.add_tooltips()

        # Enable hover detection
        from kivy.core.window import Window
        Window.bind(mouse_pos=self.on_mouse_pos)

        # Fade in animation on load
        self.opacity = 0
        from kivy.animation import Animation
        Animation(opacity=1, duration=0.4).start(self)

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
        """Creates and adds labels to the issue box with modern styling."""
        # Icon at the top (using MDIcon)
        if os.environ.get("CI") != "true":
            self.icon_label = MDIcon(
                icon=self.gradient_colors["icon"],
                font_size="32sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.9),  # White with slight transparency
                size_hint_y=None,
                height="40dp",
            )
            self.add_widget(self.icon_label)

        # Title label (smaller, above the number)
        self.title_label = MDLabel(
            text=self.title.replace("Query ", ""),  # Simplified title
            font_style="Caption",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),  # White with transparency
            size_hint_y=None,
            height="20dp",
        )

        # Big bold number in the center
        self.issue_label = MDLabel(
            text="--",
            font_style="H2",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Pure white
            bold=True,
            size_hint_y=None,
            height="60dp",
        )

        # JQL query description at the bottom (subtle)
        query_lines = self.jql_query.count("\n") + 1
        label_height = max(24, query_lines * 18)
        self.jql_label = MDLabel(
            text=self.jql_query,
            font_style="Caption",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.6),  # White with more transparency
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
        """Updates the issue count label with animation."""
        self.hide_loading()

        # Animate the number change
        old_count = 0
        try:
            old_count = int(self.issue_label.text) if self.issue_label.text.isdigit() else 0
        except:
            old_count = 0

        # If count changed, animate it
        if old_count != count and count > 0:
            self.animate_count(old_count, count)
        else:
            self.issue_label.text = str(count)

    def animate_count(self, start, end):
        """Animate counting up from start to end."""
        from kivy.clock import Clock
        duration = 0.5  # Animation duration in seconds
        steps = min(abs(end - start), 20)  # Max 20 steps
        interval = duration / steps if steps > 0 else 0

        def update_step(dt):
            if not hasattr(self, '_current_count'):
                self._current_count = start

            step_size = (end - start) / steps
            self._current_count += step_size

            if (step_size > 0 and self._current_count >= end) or (step_size < 0 and self._current_count <= end):
                self.issue_label.text = str(end)
                return False  # Stop the clock
            else:
                self.issue_label.text = str(int(self._current_count))
                return True  # Continue

        if steps > 0:
            Clock.schedule_interval(update_step, interval)
        else:
            self.issue_label.text = str(end)

    def update_label_error(self, error_message):
        """Updates the label with an error message."""
        self.hide_loading()  # Hide loading when error occurs
        self.issue_label.text = error_message
        self.issue_label.theme_text_color = "Error"  # Show error in red

    def on_mouse_pos(self, window, pos):
        """Track mouse position for hover effects."""
        if not self.get_root_window():
            return

        from kivy.core.window import Window
        # Check if mouse is over this widget
        if self.collide_point(*self.to_widget(*pos)):
            if not hasattr(self, '_is_hovered') or not self._is_hovered:
                self._is_hovered = True
                Window.set_system_cursor('hand')
                self.on_hover_enter()
        else:
            if hasattr(self, '_is_hovered') and self._is_hovered:
                self._is_hovered = False
                Window.set_system_cursor('arrow')
                self.on_hover_leave()

    def on_hover_enter(self):
        """Add glow effect on hover with elevation animation."""
        from kivy.animation import Animation
        # Increase elevation for glow effect
        Animation(elevation=16, duration=0.15).start(self)

    def on_hover_leave(self):
        """Remove glow effect when not hovering."""
        from kivy.animation import Animation
        # Return to normal elevation
        Animation(elevation=8, duration=0.15).start(self)
        # Ensure background color is maintained
        self.md_bg_color = self.gradient_colors["start"]

    def update_ui_colors(self, theme_style):
        """Update colors - gradient tiles work best with dark theme."""
        # Keep the gradient background - looks best on dark backgrounds
        self.md_bg_color = self.gradient_colors["start"]

        # Text is always white on gradient backgrounds
        text_color = (1, 1, 1, 1)

        if self.issue_label:
            self.issue_label.text_color = text_color
        if self.title_label:
            self.title_label.text_color = (1, 1, 1, 0.8)
        if self.jql_label:
            self.jql_label.text_color = (1, 1, 1, 0.6)
        if self.icon_label:
            self.icon_label.text_color = (1, 1, 1, 0.9)
