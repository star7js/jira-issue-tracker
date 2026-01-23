from typing import Optional, Dict, Any
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .logging_config import get_logger

# Configure logging
logger = get_logger(__name__)

# Constants
DEFAULT_REQUEST_TIMEOUT = 10  # seconds
RETRY_TOTAL = 3
RETRY_BACKOFF_FACTOR = 1
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]


class SafeRequests:
    """A wrapper around requests with additional security and error handling."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self._setup_retry_strategy()

    def _setup_retry_strategy(self) -> None:
        """Setup retry strategy for failed requests."""
        retry_strategy = Retry(
            total=RETRY_TOTAL,
            status_forcelist=RETRY_STATUS_CODES,
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=RETRY_BACKOFF_FACTOR,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = DEFAULT_REQUEST_TIMEOUT,
        **kwargs: Any,
    ) -> requests.Response:
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

    def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: int = DEFAULT_REQUEST_TIMEOUT,
        **kwargs: Any,
    ) -> requests.Response:
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
