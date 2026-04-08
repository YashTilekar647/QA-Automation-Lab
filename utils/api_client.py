"""
api_client.py – A simple wrapper around the `requests` library.

This module provides a reusable APIClient class so that every test file
doesn't have to repeat the same boilerplate (base URL, headers, logging).
"""

import logging
import requests

# Set up a logger for this module
logger = logging.getLogger(__name__)


class APIClient:
    """Lightweight HTTP client for interacting with a REST API."""

    def __init__(self, base_url: str):
        """
        Initialize the client with a base URL.

        Args:
            base_url: Root URL of the API (e.g. "https://jsonplaceholder.typicode.com").
        """
        self.base_url = base_url.rstrip("/")
        # A Session object keeps connections alive and lets us set defaults.
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ---- HTTP helper methods ------------------------------------------------

    def get(self, endpoint: str, params: dict = None):
        """Send a GET request and return the Response object."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("GET  %s  params=%s", url, params)
        response = self.session.get(url, params=params)
        logger.info("Response %s (%d bytes)", response.status_code, len(response.content))
        return response

    def post(self, endpoint: str, json_data: dict = None):
        """Send a POST request with a JSON body."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("POST %s  body=%s", url, json_data)
        response = self.session.post(url, json=json_data)
        logger.info("Response %s", response.status_code)
        return response

    def put(self, endpoint: str, json_data: dict = None):
        """Send a PUT request with a JSON body."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("PUT  %s  body=%s", url, json_data)
        response = self.session.put(url, json=json_data)
        logger.info("Response %s", response.status_code)
        return response

    def delete(self, endpoint: str):
        """Send a DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("DELETE %s", url)
        response = self.session.delete(url)
        logger.info("Response %s", response.status_code)
        return response
