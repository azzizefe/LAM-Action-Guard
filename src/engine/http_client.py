"""
LAM-Action-Guard HTTP Client
Handles all HTTP requests with proper error handling and rate limiting.
"""

import time
import json
from typing import Dict, Any, Optional
from urllib.parse import urljoin, urlparse

# Note: In production, use 'requests' library
# This is a simplified mock for demonstration

class HTTPClient:
    """HTTP Client with rate limiting and error handling."""

    def __init__(self, timeout: int = 10, rate_limit: float = 1.0):
        self.timeout = timeout
        self.rate_limit = rate_limit  # requests per second
        self.last_request_time = 0
        self.session_headers = {
            "User-Agent": "LAM-Action-Guard/1.0",
            "Accept": "text/html,application/json",
            "Accept-Language": "en-US,en;q=0.9"
        }

    def _rate_limit_wait(self) -> None:
        """Wait if needed to respect rate limiting."""
        if self.rate_limit > 0:
            elapsed = time.time() - self.last_request_time
            wait_time = (1.0 / self.rate_limit) - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
        self.last_request_time = time.time()

    def get(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform a GET request.
        
        In production, this would use the 'requests' library.
        This is a mock implementation for demonstration.
        """
        self._rate_limit_wait()
        
        # Mock response for demonstration
        print(f"[→] GET {url}")
        return {
            "status_code": 200,
            "url": url,
            "headers": {"content-type": "text/html"},
            "text": "<html><body>Mock Response</body></html>",
            "elapsed": 0.1
        }

    def post(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform a POST request.
        """
        self._rate_limit_wait()
        
        print(f"[→] POST {url}")
        return {
            "status_code": 200,
            "url": url,
            "headers": {"content-type": "application/json"},
            "text": json.dumps({"status": "ok"}),
            "elapsed": 0.15
        }

    def inject_payload(self, url: str, payload: str, injection_point: str = "query") -> Dict[str, Any]:
        """
        Inject a payload into the URL for security testing.
        
        Args:
            url: Target URL
            payload: The payload to inject
            injection_point: Where to inject ('query', 'path', 'body')
        """
        self._rate_limit_wait()
        
        if injection_point == "query":
            # Add payload as query parameter
            separator = "&" if "?" in url else "?"
            test_url = f"{url}{separator}test={payload}"
        elif injection_point == "path":
            test_url = urljoin(url, payload)
        else:
            test_url = url
            
        print(f"[→] INJECT {test_url[:80]}...")
        
        # Mock response - in real scenario, analyze actual response
        return {
            "status_code": 200,
            "url": test_url,
            "text": f"<html><body>Response for {payload}</body></html>",
            "reflected": payload in f"<html><body>Response for {payload}</body></html>",
            "elapsed": 0.2
        }

    def check_connection(self, url: str) -> bool:
        """Check if target is reachable."""
        try:
            response = self.get(url)
            return response.get("status_code", 0) < 500
        except Exception:
            return False
