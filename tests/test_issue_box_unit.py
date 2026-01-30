import unittest
from unittest.mock import patch, MagicMock
import os


class TestIssueBoxUnit(unittest.TestCase):
    """Unit tests for IssueBox module-level code."""

    def test_themes_dict_exists(self):
        """Test that THEMES dictionary is properly defined"""
        from jira_tracker.issue_box import THEMES

        self.assertIsInstance(THEMES, dict)
        self.assertIn("Default", THEMES)
        self.assertIn("Ocean", THEMES)
        self.assertIn("Sunset", THEMES)
        self.assertIn("Forest", THEMES)
        self.assertIn("Nord", THEMES)

    def test_theme_structure_default(self):
        """Test that Default theme has correct structure"""
        from jira_tracker.issue_box import THEMES

        default_theme = THEMES["Default"]
        self.assertIn("Query One", default_theme)
        self.assertIn("Query Two", default_theme)
        self.assertIn("Query Three", default_theme)
        self.assertIn("Query Four", default_theme)

        # Check structure of Query One
        query_one = default_theme["Query One"]
        self.assertIn("start", query_one)
        self.assertIn("end", query_one)
        self.assertIn("icon", query_one)

    def test_theme_structure_ocean(self):
        """Test that Ocean theme has correct structure"""
        from jira_tracker.issue_box import THEMES

        ocean_theme = THEMES["Ocean"]
        self.assertIn("Query One", ocean_theme)
        self.assertIn("icon", ocean_theme["Query One"])

    def test_theme_structure_sunset(self):
        """Test that Sunset theme has correct structure"""
        from jira_tracker.issue_box import THEMES

        sunset_theme = THEMES["Sunset"]
        self.assertIn("Query One", sunset_theme)
        self.assertIn("icon", sunset_theme["Query One"])

    def test_theme_structure_forest(self):
        """Test that Forest theme has correct structure"""
        from jira_tracker.issue_box import THEMES

        forest_theme = THEMES["Forest"]
        self.assertIn("Query One", forest_theme)
        self.assertIn("icon", forest_theme["Query One"])

    def test_theme_structure_nord(self):
        """Test that Nord theme has correct structure"""
        from jira_tracker.issue_box import THEMES

        nord_theme = THEMES["Nord"]
        self.assertIn("Query One", nord_theme)
        self.assertIn("icon", nord_theme["Query One"])

    def test_light_text_color_exists(self):
        """Test that LIGHT_TEXT_COLOR is defined"""
        from jira_tracker.issue_box import LIGHT_TEXT_COLOR

        self.assertIsNotNone(LIGHT_TEXT_COLOR)
        self.assertIsInstance(LIGHT_TEXT_COLOR, (tuple, list))

    def test_dark_text_color_exists(self):
        """Test that DARK_TEXT_COLOR is defined"""
        from jira_tracker.issue_box import DARK_TEXT_COLOR

        self.assertIsNotNone(DARK_TEXT_COLOR)
        self.assertIsInstance(DARK_TEXT_COLOR, (tuple, list))

    def test_all_themes_have_four_queries(self):
        """Test that all themes have all four queries defined"""
        from jira_tracker.issue_box import THEMES

        expected_queries = ["Query One", "Query Two", "Query Three", "Query Four"]

        for theme_name, theme in THEMES.items():
            with self.subTest(theme=theme_name):
                for query in expected_queries:
                    self.assertIn(query, theme)

    def test_all_query_configs_have_icons(self):
        """Test that all query configurations have icons"""
        from jira_tracker.issue_box import THEMES

        for theme_name, theme in THEMES.items():
            for query_name, config in theme.items():
                with self.subTest(theme=theme_name, query=query_name):
                    self.assertIn("icon", config)
                    self.assertIsInstance(config["icon"], str)

    def test_ci_environment_mock_classes(self):
        """Test that CI environment uses mock classes"""
        # Store original CI value
        original_ci = os.environ.get("CI")

        try:
            # Set CI environment variable
            os.environ["CI"] = "true"

            # Reload the module to trigger CI path
            import importlib
            import jira_tracker.issue_box

            importlib.reload(jira_tracker.issue_box)

            # Verify that basic module constants still work in CI mode
            self.assertIsNotNone(jira_tracker.issue_box.THEMES)
            self.assertIsInstance(jira_tracker.issue_box.THEMES, dict)

        finally:
            # Restore original CI value (don't delete it, as it's set in GitHub Actions)
            if original_ci is not None:
                os.environ["CI"] = original_ci
            # If there was no original CI value and we're not actually in CI, clean up
            elif "CI" in os.environ and os.environ.get("GITHUB_ACTIONS") != "true":
                del os.environ["CI"]

    def test_theme_colors_are_tuples_or_lists(self):
        """Test that all theme colors are tuples or lists"""
        from jira_tracker.issue_box import THEMES

        for theme_name, theme in THEMES.items():
            for query_name, config in theme.items():
                with self.subTest(theme=theme_name, query=query_name):
                    self.assertIn("start", config)
                    self.assertIn("end", config)
                    # Colors should be iterable (tuple or list)
                    self.assertIsInstance(config["start"], (tuple, list))
                    self.assertIsInstance(config["end"], (tuple, list))

    def test_all_themes_have_same_queries(self):
        """Test that all themes have the same query names"""
        from jira_tracker.issue_box import THEMES

        # Get query names from Default theme
        default_queries = set(THEMES["Default"].keys())

        # Check all other themes have the same queries
        for theme_name, theme in THEMES.items():
            with self.subTest(theme=theme_name):
                self.assertEqual(set(theme.keys()), default_queries)

    def test_theme_count(self):
        """Test that there are exactly 5 themes"""
        from jira_tracker.issue_box import THEMES

        self.assertEqual(len(THEMES), 5)

    def test_query_count_per_theme(self):
        """Test that each theme has exactly 4 queries"""
        from jira_tracker.issue_box import THEMES

        for theme_name, theme in THEMES.items():
            with self.subTest(theme=theme_name):
                self.assertEqual(len(theme), 4)

    def test_icon_names_are_strings(self):
        """Test that all icon names are non-empty strings"""
        from jira_tracker.issue_box import THEMES

        for theme_name, theme in THEMES.items():
            for query_name, config in theme.items():
                with self.subTest(theme=theme_name, query=query_name):
                    icon = config["icon"]
                    self.assertIsInstance(icon, str)
                    self.assertGreater(len(icon), 0)


if __name__ == "__main__":
    unittest.main()
