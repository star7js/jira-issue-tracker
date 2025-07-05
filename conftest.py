import os

# Set environment variables for CI testing
if os.environ.get("CI") == "true":
    # Ensure we're in CI mode
    os.environ["CI"] = "true"
    # Disable Kivy window creation
    os.environ["KIVY_WINDOW"] = "dummy"
