"""
API client using Playwright's APIRequestContext.
Provides a thin wrapper for HTTP calls against the Sauce Demo API,
enabling API-level test setup, teardown, and validation without UI.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.sync_api import APIRequestContext, APIResponse


class APIClient:
    def __init__(self, request: APIRequestContext, base_url: str, logger: logging.Logger) -> None:
        self._request = request
        self._base_url = base_url.rstrip("/")
        self.logger = logger

    # ------------------------------------------------------------------
    # Core HTTP methods
    # ------------------------------------------------------------------

    def get(self, path: str, **kwargs: Any) -> APIResponse:
        url = f"{self._base_url}{path}"
        self.logger.info(f"GET {url}")
        response = self._request.get(url, **kwargs)
        self._log_response(response)
        return response

    def post(self, path: str, **kwargs: Any) -> APIResponse:
        url = f"{self._base_url}{path}"
        self.logger.info(f"POST {url}")
        response = self._request.post(url, **kwargs)
        self._log_response(response)
        return response

    def put(self, path: str, **kwargs: Any) -> APIResponse:
        url = f"{self._base_url}{path}"
        self.logger.info(f"PUT {url}")
        response = self._request.put(url, **kwargs)
        self._log_response(response)
        return response

    def delete(self, path: str, **kwargs: Any) -> APIResponse:
        url = f"{self._base_url}{path}"
        self.logger.info(f"DELETE {url}")
        response = self._request.delete(url, **kwargs)
        self._log_response(response)
        return response

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _log_response(self, response: APIResponse) -> None:
        self.logger.info(f"Response: {response.status} {response.url}")

    @staticmethod
    def assert_status(response: APIResponse, expected: int) -> None:
        actual = response.status
        assert actual == expected, (
            f"Expected HTTP {expected}, got {actual}. URL: {response.url}"
        )

    @staticmethod
    def assert_ok(response: APIResponse) -> None:
        assert response.ok, (
            f"Expected 2xx response, got {response.status}. URL: {response.url}"
        )
