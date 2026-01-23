from typing import Dict, Optional, Any
import base64
import requests
from dotenv import load_dotenv, get_key
from .security import safe_requests
from .logging_config import get_logger

# Load environment variables
load_dotenv()

# Configure logging
logger = get_logger(__name__)

# Constants
DEFAULT_API_REQUEST_INTERVAL = 3600  # 1 hour in seconds
DEFAULT_REQUEST_TIMEOUT = 10  # seconds

# Global constants
JIRA_SITE_URL = get_key(".env", "JIRA_SITE_URL") or ""
JIRA_EMAIL = get_key(".env", "JIRA_EMAIL") or ""
JIRA_API_TOKEN = get_key(".env", "JIRA_API_TOKEN") or ""
# Use API v3 search/approximate-count for Cloud (POST), v2 search for Server (GET)
JIRA_API_ENDPOINT_CLOUD = "/rest/api/3/search/approximate-count"
JIRA_API_ENDPOINT_SERVER = "/rest/api/2/search"

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


def create_request_headers_cloud() -> Dict[str, str]:
    """Create the request headers for Jira Cloud using Basic Auth."""
    auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    auth_bytes = auth_string.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")
    return {
        "Authorization": f"Basic {base64_string}",
        "Content-Type": "application/json",
    }


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


def execute_request_cloud(
    url: str, headers: Dict[str, str], jql_query: str
) -> Optional[Dict[str, Any]]:
    """Execute the request and return the response for Jira Cloud using POST."""
    try:
        payload = {"jql": jql_query}
        response = safe_requests.post(
            url, headers=headers, json=payload, timeout=DEFAULT_REQUEST_TIMEOUT
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

    # Use Cloud auth and endpoint if email is configured, otherwise use Server
    if JIRA_EMAIL:
        # Cloud uses POST to /search/approximate-count
        url = create_request_url(JIRA_API_ENDPOINT_CLOUD)
        headers = create_request_headers_cloud()
        response = execute_request_cloud(url, headers, jql_query)
        # approximate-count returns {"count": number}
        return response.get("count", 0) if response else 0
    else:
        # Server uses GET to /search with query params
        url = create_request_url(JIRA_API_ENDPOINT_SERVER)
        headers = create_request_headers_server()
        query_params = {"jql": jql_query}
        response = execute_request_server(url, headers, query_params)
        # Server returns {"total": number, "issues": [...]}
        return response.get("total", 0) if response else 0


# Example usage
if __name__ == "__main__":
    jql_query = "project = TEST"
    result = get_jql_query_results(jql_query)
    logger.info(f"Query Result: {result}")
