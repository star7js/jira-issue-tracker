import os
import pytest
from unittest.mock import patch, MagicMock

# Set environment variables for CI testing
if os.environ.get("CI") == "true":
    # Ensure we're in CI mode
    os.environ["CI"] = "true"
    # Disable Kivy window creation
    os.environ["KIVY_WINDOW"] = "dummy"

@pytest.fixture(autouse=True, scope="session")
def patch_kivy_window_and_eventloop():
    """
    Patch Kivy's Window and EventLoop to prevent window creation in headless/CI environments.
    Applies to all tests automatically.
    """
    with patch("kivy.core.window.Window", new=MagicMock()):
        with patch("kivy.base.EventLoop.ensure_window", new=MagicMock()):
            yield
