"""Mock classes for CI environment where Kivy/KivyMD are not available."""


class MDApp:
    """Mock MDApp for CI testing."""

    def __init__(self):
        pass

    def run(self):
        pass

    @staticmethod
    def get_running_app():
        return None


class MDRaisedButton:
    """Mock MDRaisedButton for CI testing."""

    def __init__(self, **kwargs):
        pass


class MDTooltip:
    """Mock MDTooltip for CI testing."""

    def __init__(self, **kwargs):
        pass


class MDLabel:
    """Mock MDLabel for CI testing."""

    def __init__(self, **kwargs):
        pass


class JiraIssueTracker:
    """Mock JiraIssueTracker for CI testing."""

    def __init__(self):
        pass


class JiraConnectionSettingsPopup:
    """Mock JiraConnectionSettingsPopup for CI testing."""

    def __init__(self):
        pass
