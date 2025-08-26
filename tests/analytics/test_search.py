"""Tests for analytics search operations."""

from __future__ import annotations

import pytest

from patsnap_pythonSDK.errors import ApiError, AuthError
from tests.shared import FakeResponse, FakeSession, make_client_with_session, create_oauth_payload, create_error_oauth_payload


def test_query_count_success():
    """Test successful analytics query search count."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "total_search_result_count": 1000
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_count(
        query_text="TACD: virtual reality",
        collapse_by="PBD",
        stemming=0
    )

    # Verify response structure
    assert resp.total_search_result_count == 1000

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["query_text"] == "TACD: virtual reality"
    assert json_data["collapse_by"] == "PBD"
    assert json_data["stemming"] == 0

    client.close()


def test_query_count_with_all_parameters():
    """Test analytics query search count with all parameters."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "total_search_result_count": 2500
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_count(
        query_text="TACD: artificial intelligence AND machine learning",
        collapse_order="LATEST",
        collapse_by="APD",
        collapse_order_authority=["US", "CN", "EP"],
        stemming=1,
        collapse_type="DOCDB"
    )

    assert resp.total_search_result_count == 2500
    
    # Verify all parameters were sent
    json_data = session.last_request.json
    assert json_data["query_text"] == "TACD: artificial intelligence AND machine learning"
    assert json_data["collapse_order"] == "LATEST"
    assert json_data["collapse_by"] == "APD"
    assert json_data["collapse_order_authority"] == ["US", "CN", "EP"]
    assert json_data["stemming"] == 1
    assert json_data["collapse_type"] == "DOCDB"

    client.close()


def test_query_count_api_error():
    """Test API error handling in analytics query search count."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": False, 
        "error_code": 68300004, 
        "error_msg": "Invalid parameter!"
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    with pytest.raises(ApiError):
        client.analytics.search.query_count(query_text="invalid query")

    client.close()


def test_query_count_http_error():
    """Test HTTP error handling in analytics query search count."""
    oauth_payload = create_error_oauth_payload()
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(500, None, text="server error"))
    client = make_client_with_session(session)

    with pytest.raises(ApiError):
        client.analytics.search.query_count(query_text="test query")

    client.close()


def test_query_count_validation_error():
    """Test request validation in analytics query search count."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing required parameter
    with pytest.raises(Exception):  # Pydantic validation error
        client.analytics.search.query_count()  # Missing query_text

    # Test query text too long (over 1500 characters)
    long_query = "A" * 1501
    with pytest.raises(Exception):  # Pydantic validation error
        client.analytics.search.query_count(query_text=long_query)

    client.close()


def test_query_count_minimal_parameters():
    """Test analytics query search count with minimal parameters."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "total_search_result_count": 500
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_count(query_text="blockchain")

    assert resp.total_search_result_count == 500
    
    # Verify only required parameter was sent
    json_data = session.last_request.json
    assert json_data["query_text"] == "blockchain"
    # Optional parameters should not be in the request
    assert "collapse_order" not in json_data
    assert "collapse_by" not in json_data
    assert "stemming" not in json_data

    client.close()


def test_query_count_different_collapse_types():
    """Test analytics query search count with different collapse types."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "total_search_result_count": 750
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test with INPADOC collapse type
    resp = client.analytics.search.query_count(
        query_text="renewable energy",
        collapse_type="INPADOC",
        collapse_by="AUTHORITY",
        collapse_order_authority=["CN", "US", "EP", "JP", "KR"]
    )

    assert resp.total_search_result_count == 750
    
    json_data = session.last_request.json
    assert json_data["collapse_type"] == "INPADOC"
    assert json_data["collapse_by"] == "AUTHORITY"
    assert json_data["collapse_order_authority"] == ["CN", "US", "EP", "JP", "KR"]

    client.close()


def test_query_search_success():
    """Test successful analytics query search."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "US11205304B2",
                    "apdt": 20211108,
                    "apno": "US17/521392",
                    "pbdt": 20230815,
                    "title": "Techniques for using multiple symbols to provide feedback for a sidelink transmission",
                    "inventor": "ELSHAFIE, AHMED | YANG, WEI | HOSSEINI, SEYEDKIANOUSH",
                    "patent_id": "718ead9c-4f3c-4674-8f5a-24e126827269",
                    "current_assignee": "QUALCOMM INCORPORATED",
                    "original_assignee": "QUALCOMM INCORPORATED"
                }
            ],
            "result_count": 1,
            "total_search_result_count": 1000
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_search(
        query_text="TACD: virtual reality",
        limit=10,
        sort=[{"field": "SCORE", "order": "DESC"}]
    )

    # Verify response structure
    assert resp.result_count == 1
    assert resp.total_search_result_count == 1000
    assert len(resp.results) == 1
    
    # Verify patent data
    patent = resp.results[0]
    assert patent.pn == "US11205304B2"
    assert patent.title == "Techniques for using multiple symbols to provide feedback for a sidelink transmission"
    assert patent.current_assignee == "QUALCOMM INCORPORATED"

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["query_text"] == "TACD: virtual reality"
    assert json_data["limit"] == 10
    assert json_data["sort"] == [{"field": "SCORE", "order": "DESC"}]

    client.close()


def test_query_search_with_all_parameters():
    """Test analytics query search with all parameters."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "CN123456A",
                    "apdt": 20220101,
                    "apno": "CN2022123456",
                    "pbdt": 20230101,
                    "title": "AI Patent Example",
                    "inventor": "John Doe",
                    "patent_id": "test-id-123",
                    "current_assignee": "Tech Corp",
                    "original_assignee": "Tech Corp"
                }
            ],
            "result_count": 1,
            "total_search_result_count": 500
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_search(
        query_text="TACD: artificial intelligence AND machine learning",
        offset=10,
        sort=[{"field": "PBDT_YEARMONTHDAY", "order": "DESC"}],
        collapse_order="LATEST",
        collapse_by="APD",
        collapse_order_authority=["US", "CN", "EP"],
        limit=20,
        stemming=1,
        collapse_type="DOCDB"
    )

    assert resp.result_count == 1
    assert resp.total_search_result_count == 500
    
    # Verify all parameters were sent
    json_data = session.last_request.json
    assert json_data["query_text"] == "TACD: artificial intelligence AND machine learning"
    assert json_data["offset"] == 10
    assert json_data["sort"] == [{"field": "PBDT_YEARMONTHDAY", "order": "DESC"}]
    assert json_data["collapse_order"] == "LATEST"
    assert json_data["collapse_by"] == "APD"
    assert json_data["collapse_order_authority"] == ["US", "CN", "EP"]
    assert json_data["limit"] == 20
    assert json_data["stemming"] == 1
    assert json_data["collapse_type"] == "DOCDB"

    client.close()


def test_query_search_validation_error():
    """Test request validation in analytics query search."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"results": [], "result_count": 0, "total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing required parameter
    with pytest.raises(Exception):  # Pydantic validation error
        client.analytics.search.query_search()  # Missing query_text

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.analytics.search.query_search(query_text="test", limit=2000)  # > 1000

    client.close()


def test_query_filter_success():
    """Test successful analytics query filter."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": [
            {
                "assignee": [
                    {
                        "name": "APPLE INC.",
                        "count": 2509
                    },
                    {
                        "name": "GOOGLE LLC",
                        "count": 1834
                    }
                ]
            }
        ],
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_filter(
        query="TTL:汽车",
        field="ASSIGNEE",
        offset=0,
        limit=20
    )

    # Verify response structure
    assert len(resp) == 1
    assert hasattr(resp[0], 'assignee')
    assert len(resp[0].assignee) == 2
    
    # Verify assignee data
    assignees = resp[0].assignee
    assert assignees[0].name == "APPLE INC."
    assert assignees[0].count == 2509
    assert assignees[1].name == "GOOGLE LLC"
    assert assignees[1].count == 1834

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["query"] == "TTL:汽车"
    assert json_data["field"] == "ASSIGNEE"
    assert json_data["offset"] == 0
    assert json_data["limit"] == 20

    client.close()


def test_query_filter_with_all_parameters():
    """Test analytics query filter with all parameters."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": [
            {
                "authority": [
                    {
                        "name": "CN",
                        "count": 15000
                    },
                    {
                        "name": "US",
                        "count": 12000
                    }
                ]
            }
        ],
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.analytics.search.query_filter(
        query="TACD: artificial intelligence",
        field="AUTHORITY",
        offset=10,
        limit=50,
        collapse_order="LATEST",
        collapse_by="APD",
        collapse_order_authority=["US", "CN", "EP"],
        stemming=1,
        lang="en",
        collapse_type="DOCDB"
    )

    assert len(resp) == 1
    assert hasattr(resp[0], 'authority')
    assert len(resp[0].authority) == 2
    
    # Verify all parameters were sent
    json_data = session.last_request.json
    assert json_data["query"] == "TACD: artificial intelligence"
    assert json_data["field"] == "AUTHORITY"
    assert json_data["offset"] == 10
    assert json_data["limit"] == 50
    assert json_data["collapse_order"] == "LATEST"
    assert json_data["collapse_by"] == "APD"
    assert json_data["collapse_order_authority"] == ["US", "CN", "EP"]
    assert json_data["stemming"] == 1
    assert json_data["lang"] == "en"
    assert json_data["collapse_type"] == "DOCDB"

    client.close()


def test_query_filter_validation_error():
    """Test request validation in analytics query filter."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": []
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing required parameters
    with pytest.raises(Exception):  # Pydantic validation error
        client.analytics.search.query_filter()  # Missing query and field

    # Test query too long (over 800 characters)
    long_query = "A" * 801
    with pytest.raises(Exception):  # Pydantic validation error
        client.analytics.search.query_filter(
            query=long_query,
            field="ASSIGNEE",
            offset=0
        )

    client.close()
