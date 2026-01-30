import unittest
from unittest.mock import patch, MagicMock
import logging
from jira_tracker.logging_config import setup_logging, get_logger


class TestLoggingConfig(unittest.TestCase):

    def setUp(self):
        """Reset logging configured flag before each test"""
        import jira_tracker.logging_config
        jira_tracker.logging_config._logging_configured = False

    def test_setup_logging_configures_logger(self):
        """Test that setup_logging configures the logger"""
        with patch("logging.basicConfig") as mock_config:
            setup_logging()
            mock_config.assert_called_once()

    def test_setup_logging_only_runs_once(self):
        """Test that setup_logging only configures once"""
        with patch("logging.basicConfig") as mock_config:
            setup_logging()
            setup_logging()
            # Should only be called once
            self.assertEqual(mock_config.call_count, 1)

    def test_setup_logging_custom_level(self):
        """Test setup_logging with custom level"""
        with patch("logging.basicConfig") as mock_config:
            setup_logging(level=logging.DEBUG)
            mock_config.assert_called_once()
            # Verify level was passed
            call_kwargs = mock_config.call_args[1]
            self.assertEqual(call_kwargs["level"], logging.DEBUG)

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance"""
        logger = get_logger("test_module")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_module")

    def test_get_logger_calls_setup_logging(self):
        """Test that get_logger calls setup_logging"""
        with patch("jira_tracker.logging_config.setup_logging") as mock_setup:
            with patch("logging.getLogger") as mock_get:
                mock_logger = MagicMock()
                mock_get.return_value = mock_logger

                logger = get_logger("test_module")

                mock_setup.assert_called_once()
                mock_get.assert_called_once_with("test_module")


if __name__ == "__main__":
    unittest.main()
