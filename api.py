from typing import Dict, Optional, Any
import requests
from dotenv import load_dotenv, get_key
from security import safe_requests
from logging_config import get_logger

# Load environment variables
load_dotenv()

# Configure logging
logger = get_logger(__name__)

# Constants
DEFAULT_API_REQUEST_INTERVAL = 3600  # 1 hour in seconds
DEFAULT_REQUEST_TIMEOUT = 10  # seconds

# Global constants
JIRA_SITE_URL = get_key(".env", "JIRA_SITE_URL") or ""
JIRA_API_TOKEN = get_key(".env", "JIRA_API_TOKEN") or ""
JIRA_API_ENDPOINT = "/rest/api/latest/search"

# JQL Queries from .env file with defaults
JQL_QUERY_ONE = get_key(".env", "JQL_QUERY_ONE") or ""
JQL_QUERY_TWO = get_key(".env", "JQL_QUERY_TWO") or ""
JQL_QUERY_THREE = get_key(".env", "JQL_QUERY_THREE") or ""
JQL_QUERY_FOUR = get_key(".env", "JQL_QUERY_FOUR") or ""


def create_request_url(endpoint: str) -> str:
    """Create the full request URL."""
    return f"{JIRA_SITE_URL}{endpoint}"


def create_request_headers_server() -> Dict[str, str]:
    """Create the request headers. For server or data center only."""
    return {"Authorization": f"Bearer {JIRA_API_TOKEN}"}


def execute_request_server(
    url: str, headers: Dict[str, str], query_params: Dict[str, str]
) -> Optional[Dict[str, Any]]:
    """Execute the request and return the response. For server or data center only."""
    try:
        response = safe_requests.get(
            url, headers=headers, params=query_params, timeout=DEFAULT_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        handle_request_error(error)
        return None


def handle_request_error(error: requests.RequestException) -> None:
    """Handle different types of request errors."""
    if isinstance(error, requests.HTTPError):
        logger.error(f"HTTP error: {error}")
    elif isinstance(error, requests.ConnectionError):
        logger.error("Failed to connect to the server.")
    elif isinstance(error, requests.Timeout):
        logger.error("Request timed out.")
    elif isinstance(error, requests.TooManyRedirects):
        logger.error("Too many redirects.")
    else:
        logger.error(f"An error occurred: {error}")


def validate_jql_query(jql_query: str) -> bool:
    """Validate JQL query before sending to API."""
    if not jql_query or not isinstance(jql_query, str):
        logger.warning("Invalid JQL query: must be a non-empty string")
        return False

    # Strip whitespace
    jql_query = jql_query.strip()

    if not jql_query:
        logger.warning("Invalid JQL query: empty after stripping whitespace")
        return False

    # Check for suspicious patterns that might indicate injection attempts
    suspicious_patterns = ["';", "--", "/*", "*/", "xp_", "exec(", "eval("]
    for pattern in suspicious_patterns:
        if pattern in jql_query.lower():
            logger.warning(f"Suspicious pattern detected in JQL query: {pattern}")
            return False

    return True


def get_jql_query_results(jql_query: str) -> int:
    """Fetch issue count for a JQL query."""
    if not validate_jql_query(jql_query):
        logger.error(f"Invalid JQL query rejected: {jql_query}")
        return 0

    url = create_request_url(JIRA_API_ENDPOINT)
    headers = create_request_headers_server()
    query_params = {"jql": jql_query}
    response = execute_request_server(url, headers, query_params)
    return response.get("total", 0) if response else 0


# Example usage
if __name__ == "__main__":
    jql_query = "project = TEST"
    result = get_jql_query_results(jql_query)
    logger.info(f"Query Result: {result}")
