"""Centralized logging configuration for the application."""

import logging
import sys

# Flag to ensure logging is only configured once
_logging_configured = False


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the entire application.

    Args:
        level: The logging level to use (default: logging.INFO)
    """
    global _logging_configured

    if _logging_configured:
        return

    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.

    Args:
        name: The name of the logger (typically __name__)

    Returns:
        A configured logger instance
    """
    setup_logging()
    return logging.getLogger(name)
