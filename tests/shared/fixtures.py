"""
Shared test fixtures and utilities for the Patsnap SDK test suite.

These utilities provide common functionality for mocking HTTP responses
and creating test clients across all test modules.
"""

from __future__ import annotations

from typing import Any, Dict
from types import SimpleNamespace

from patsnap_pythonSDK.client import PatsnapClient


class FakeResponse:
    """Mock HTTP response for testing."""
    
    def __init__(self, status_code: int, json_data: Dict[str, Any] | None = None, text: str = "") -> None:
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self) -> Dict[str, Any]:
        if self._json is None:
            raise ValueError("no json")
        return self._json


class FakeSession:
    """A simple fake of requests.Session with programmable responses.

    It inspects the URL to decide which response to return (oauth vs business).
    """

    def __init__(self, oauth_response: FakeResponse, business_response: FakeResponse):
        self._oauth_response = oauth_response
        self._business_response = business_response
        self.last_request = SimpleNamespace(url=None, headers=None, params=None, json=None)

    def post(self, url, *, headers=None, params=None, data=None, json=None, timeout=None, auth=None):
        self.last_request = SimpleNamespace(url=url, headers=headers, params=params, json=json, data=data, auth=auth)
        if url.endswith("/oauth/token"):
            return self._oauth_response
        return self._business_response

    def close(self) -> None:  # pragma: no cover - not used in unit assertions
        pass


def make_client_with_session(session: FakeSession) -> PatsnapClient:
    """Create a test client with a fake session."""
    return PatsnapClient(client_id="client-id", client_secret="client-secret", session=session)


def create_oauth_payload() -> Dict[str, Any]:
    """Create a standard OAuth response payload for tests."""
    return {
        "token": "token_example",
        "token_type": "BearerToken",
        "expires_in": 1799,
        "status": "approved",
        "issued_at": "1692347672874",
    }


def create_error_oauth_payload() -> Dict[str, Any]:
    """Create a minimal OAuth response payload for error tests."""
    return {
        "token": "t", 
        "token_type": "BearerToken", 
        "expires_in": 1000, 
        "status": "approved", 
        "issued_at": "1692347672874"
    }
