import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SafeRequests:
    """A wrapper around requests with additional security and error handling."""

    def __init__(self):
        self.session = requests.Session()
        self._setup_retry_strategy()

    def _setup_retry_strategy(self):
        """Setup retry strategy for failed requests."""
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url, headers=None, params=None, timeout=10, **kwargs):
        """Perform a GET request with security measures."""
        try:
            # Validate URL
            if not url or not isinstance(url, str):
                raise ValueError("Invalid URL provided")

            # Ensure HTTPS for production URLs (optional security measure)
            if (
                url.startswith("http://")
                and "localhost" not in url
                and "127.0.0.1" not in url
            ):
                logger.warning("Using HTTP instead of HTTPS for non-localhost URL")

            # Perform the request
            response = self.session.get(
                url, headers=headers, params=params, timeout=timeout, **kwargs
            )

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during request: {e}")
            raise

    def post(self, url, headers=None, data=None, json=None, timeout=10, **kwargs):
        """Perform a POST request with security measures."""
        try:
            # Validate URL
            if not url or not isinstance(url, str):
                raise ValueError("Invalid URL provided")

            # Perform the request
            response = self.session.post(
                url, headers=headers, data=data, json=json, timeout=timeout, **kwargs
            )

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during request: {e}")
            raise


# Create a global instance
safe_requests = SafeRequests()
