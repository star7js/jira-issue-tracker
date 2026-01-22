"""Validation for .env file configuration."""

import os
from typing import List, Tuple
from logging_config import get_logger

logger = get_logger(__name__)

# Required environment variables
REQUIRED_ENV_VARS = ["JIRA_SITE_URL", "JIRA_API_TOKEN"]

# Optional environment variables
OPTIONAL_ENV_VARS = [
    "JQL_QUERY_ONE",
    "JQL_QUERY_TWO",
    "JQL_QUERY_THREE",
    "JQL_QUERY_FOUR",
    "JIRA_SERVER",
]


def validate_env_file() -> Tuple[bool, List[str]]:
    """
    Validate that .env file exists and contains required variables.

    Returns:
        Tuple of (is_valid, list_of_missing_vars)
    """
    env_file_path = ".env"

    # Check if .env file exists
    if not os.path.exists(env_file_path):
        logger.error(f".env file not found at {os.path.abspath(env_file_path)}")
        return False, ["File .env does not exist"]

    # Check if file is readable
    if not os.access(env_file_path, os.R_OK):
        logger.error(f".env file exists but is not readable")
        return False, ["File .env is not readable"]

    # Load and check required variables
    from dotenv import load_dotenv, get_key

    load_dotenv()

    missing_vars = []
    for var in REQUIRED_ENV_VARS:
        value = get_key(env_file_path, var)
        if not value or not value.strip():
            missing_vars.append(var)
            logger.warning(f"Required variable {var} is missing or empty")

    if missing_vars:
        return False, missing_vars

    logger.info("Environment file validation successful")
    return True, []


def validate_jira_url(url: str) -> bool:
    """
    Validate that Jira URL is properly formatted.

    Args:
        url: The Jira site URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False

    # Must start with http:// or https://
    if not url.startswith(("http://", "https://")):
        logger.warning(f"Jira URL must start with http:// or https://: {url}")
        return False

    # Should not have trailing slash
    if url.endswith("/"):
        logger.warning(f"Jira URL should not end with '/': {url}")
        return False

    return True
