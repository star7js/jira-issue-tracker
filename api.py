import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default interval for API requests in seconds
DEFAULT_API_REQUEST_INTERVAL = 60 * 60  # 1 hour

# Global constants
JIRA_SITE_URL = os.getenv('JIRA_SITE_URL')
JIRA_API_KEY = os.getenv('JIRA_API_KEY')
JIRA_API_ENDPOINT = "/rest/api/latest/search"

# Configure logging
logging.basicConfig(level=logging.INFO)


def create_request_url(endpoint):
    """Create the full request URL."""
    return f"{JIRA_SITE_URL}{endpoint}"


def create_request_headers():
    """Create the request headers."""
    return {'Authorization': f'Bearer {JIRA_API_KEY}'}


def execute_request(url, headers, query_params):
    """Execute the request and return the response."""
    try:
        response = requests.get(url, headers=headers, params=query_params, timeout=10)
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
    headers = create_request_headers()
    query_params = {"jql": jql_query}
    response = execute_request(url, headers, query_params)
    return response.get("total", 0) if response else 0


# Example usage
if __name__ == "__main__":
    jql_query = "project = TEST"
    result = get_jql_query_results(jql_query)
    logging.info(f"Query Result: {result}")
