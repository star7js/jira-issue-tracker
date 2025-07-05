import requests
import logging
from dotenv import load_dotenv, get_key
from security import safe_requests

# Load environment variables
load_dotenv()

# Default interval for API requests in seconds
DEFAULT_API_REQUEST_INTERVAL = 60 * 60  # 1 time per hour

# Global constants
JIRA_SITE_URL = get_key('.env', 'JIRA_SITE_URL') or ''
JIRA_API_TOKEN = get_key('.env', 'JIRA_API_TOKEN') or ''
JIRA_API_ENDPOINT = "/rest/api/latest/search"

# JQL Queries from .env file with defaults
JQL_QUERY_ONE = get_key('.env', 'JQL_QUERY_ONE') or ''
JQL_QUERY_TWO = get_key('.env', 'JQL_QUERY_TWO') or ''
JQL_QUERY_THREE = get_key('.env', 'JQL_QUERY_THREE') or ''
JQL_QUERY_FOUR = get_key('.env', 'JQL_QUERY_FOUR') or ''

# Configure logging
logging.basicConfig(level=logging.INFO)


def create_request_url(endpoint):
    """Create the full request URL."""
    return f"{JIRA_SITE_URL}{endpoint}"


def create_request_headers_server():
    """Create the request headers. For server or data center only."""
    return {'Authorization': f'Bearer {JIRA_API_TOKEN}'}


def execute_request_server(url, headers, query_params):
    """Execute the request and return the response. For server or data center only."""
    try:
        response = safe_requests.get(url, headers=headers, params=query_params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        handle_request_error(error)
        return None


def handle_request_error(error):
    """Handle different types of request errors."""
    if isinstance(error, requests.HTTPError):
        logging.error(f"HTTP error: {error}")
    elif isinstance(error, requests.ConnectionError):
        logging.error("Failed to connect to the server.")
    # More specific cases can be added as needed
    else:
        logging.error(f"An error occurred: {error}")


def get_jql_query_results(jql_query):
    """Fetch issue count for a JQL query."""
    url = create_request_url(JIRA_API_ENDPOINT)
    headers = create_request_headers_server()
    query_params = {"jql": jql_query}
    response = execute_request_server(url, headers, query_params)
    return response.get("total", 0) if response else 0


# Example usage
if __name__ == "__main__":
    jql_query = "project = TEST"
    result = get_jql_query_results(jql_query)
    logging.info(f"Query Result: {result}")
