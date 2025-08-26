"""
Template for creating tests for new endpoints.

Usage:
1. Copy this template to tests/{domain}/test_{category}.py
2. Replace placeholders with actual values
3. Add comprehensive test cases
"""

from __future__ import annotations

import pytest

from patsnap_pythonSDK.errors import ApiError, AuthError
from tests.shared import FakeResponse, FakeSession, make_client_with_session, create_oauth_payload, create_error_oauth_payload


def test_{method_name}_success():
    """Test successful {method_name} request."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    # Add sample response data here
                    "id": "123",
                    "title": "Sample Result",
                }
            ],
            "result_count": 1,
            "total_count": 1,
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Make the API call
    resp = client.{domain}.{category}.{method_name}(
        query="test query",
        limit=10
    )

    # Assertions
    assert resp.result_count == 1
    assert resp.total_count == 1
    assert len(resp.results) == 1
    assert resp.results[0].id == "123"

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"

    client.close()


def test_{method_name}_api_error():
    """Test API error handling."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": False, 
        "error_code": 68300004, 
        "error_msg": "Invalid parameter!"
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    with pytest.raises(ApiError):
        client.{domain}.{category}.{method_name}(query="invalid")

    client.close()


def test_{method_name}_http_error():
    """Test HTTP error handling."""
    oauth_payload = create_error_oauth_payload()
    
    session = _FakeSession(_FakeResponse(200, oauth_payload), _FakeResponse(500, None, text="server error"))
    client = make_client_with_session(session)

    with pytest.raises(ApiError):
        client.{domain}.{category}.{method_name}(query="test")

    client.close()


def test_{method_name}_validation_error():
    """Test request validation."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"results": [], "result_count": 0, "total_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test invalid parameters (adjust based on your validation rules)
    with pytest.raises(Exception):  # Pydantic validation error
        client.{domain}.{category}.{method_name}(limit=2000)  # > 1000 invalid

    client.close()
