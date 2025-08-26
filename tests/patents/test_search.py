"""Tests for patent search operations."""

from __future__ import annotations

import pytest

from patsnap_pythonSDK.errors import ApiError, AuthError
from tests.shared import FakeResponse, FakeSession, make_client_with_session, create_oauth_payload, create_error_oauth_payload


def test_search_by_number_success():
    """Test successful patent search by number."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "US11205304B2",
                    "apdt": 20211108,
                    "apno": "US17/521392",
                    "pbdt": 20230815,
                    "title": "Sample Patent Title",
                    "inventor": "John Doe",
                    "patent_id": "id-123",
                    "current_assignee": "ACME Corp",
                    "original_assignee": "ACME Corp Original",
                }
            ],
            "result_count": 1,
            "total_search_result_count": 1,
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.patents.search.by_number(pn="US11205304B2", authority=["US"], limit=10, offset=0)

    # Verify response structure
    assert resp.result_count == 1
    assert resp.total_search_result_count == 1
    assert len(resp.results) == 1
    
    # Verify patent data
    patent = resp.results[0]
    assert patent.pn == "US11205304B2"
    assert patent.apno == "US17/521392"
    assert patent.title == "Sample Patent Title"
    assert patent.inventor == "John Doe"
    assert patent.current_assignee == "ACME Corp"

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"

    client.close()


def test_search_by_number_api_error():
    """Test API error handling in patent search."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": False, 
        "error_code": 68300004, 
        "error_msg": "Invalid parameter!"
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    with pytest.raises(ApiError):
        client.patents.search.by_number(limit=10)

    client.close()


def test_search_by_number_http_error():
    """Test HTTP error handling in patent search."""
    oauth_payload = create_error_oauth_payload()
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(500, None, text="server error"))
    client = make_client_with_session(session)

    with pytest.raises(ApiError):
        client.patents.search.by_number(limit=10)

    client.close()


def test_search_by_number_validation_error():
    """Test request validation in patent search."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"results": [], "result_count": 0, "total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test invalid limit (exceeds maximum of 1000)
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_number(limit=2000)

    client.close()


def test_search_by_application_number():
    """Test patent search by application number."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "US11205304B2",
                    "apdt": 20211108,
                    "apno": "US17/521392",
                    "pbdt": 20230815,
                    "title": "Patent from Application Search",
                    "inventor": "Jane Smith",
                    "patent_id": "id-456",
                    "current_assignee": "Tech Corp",
                    "original_assignee": "Tech Corp",
                }
            ],
            "result_count": 1,
            "total_search_result_count": 1,
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.patents.search.by_number(apno="US17/521392", authority=["US"], limit=5)

    assert resp.result_count == 1
    assert resp.results[0].apno == "US17/521392"
    assert resp.results[0].title == "Patent from Application Search"

    client.close()


def test_search_by_number_multiple_authorities():
    """Test patent search with multiple authorities."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "US11205304B2",
                    "apdt": 20211108,
                    "apno": "US17/521392",
                    "pbdt": 20230815,
                    "title": "Multi-Authority Patent",
                    "inventor": "Global Inventor",
                    "patent_id": "id-789",
                    "current_assignee": "Global Corp",
                    "original_assignee": "Global Corp",
                }
            ],
            "result_count": 1,
            "total_search_result_count": 5,
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.patents.search.by_number(
        pn="US11205304B2", 
        authority=["US", "CN", "EP"], 
        limit=10
    )

    assert resp.result_count == 1
    assert resp.total_search_result_count == 5  # More results available across authorities
    
    # Verify the request included multiple authorities
    request_params = session.last_request.params
    assert "authority" in request_params
    
    client.close()


def test_original_assignee_search_success():
    """Test successful original assignee search."""
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

    resp = client.patents.search.by_original_assignee(
        application="Apple, Inc.",
        limit=50
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
    assert json_data["application"] == "Apple, Inc."
    assert json_data["limit"] == 50

    client.close()


def test_original_assignee_search_with_all_parameters():
    """Test original assignee search with all parameters."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "CN123456A",
                    "apdt": 20220301,
                    "apno": "CN202200123456",
                    "pbdt": 20230301,
                    "title": "Artificial Intelligence System",
                    "inventor": "ZHANG, WEI | LI, MING",
                    "patent_id": "abc123-def456-ghi789",
                    "current_assignee": "HUAWEI TECHNOLOGIES CO LTD",
                    "original_assignee": "HUAWEI TECHNOLOGIES CO LTD"
                }
            ],
            "result_count": 1,
            "total_search_result_count": 5000
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.patents.search.by_original_assignee(
        application="Apple OR Huawei",
        collapse_type="DOCDB",
        collapse_by="APD",
        collapse_order="LATEST",
        collapse_order_authority=["US", "CN", "EP"],
        sort=[{"field": "SCORE", "order": "DESC"}],
        offset=10,
        limit=100
    )

    assert resp.result_count == 1
    assert resp.total_search_result_count == 5000
    
    # Verify all parameters were sent
    json_data = session.last_request.json
    assert json_data["application"] == "Apple OR Huawei"
    assert json_data["collapse_type"] == "DOCDB"
    assert json_data["collapse_by"] == "APD"
    assert json_data["collapse_order"] == "LATEST"
    assert json_data["collapse_order_authority"] == ["US", "CN", "EP"]
    assert json_data["sort"] == [{"field": "SCORE", "order": "DESC"}]
    assert json_data["offset"] == 10
    assert json_data["limit"] == 100

    client.close()


def test_original_assignee_search_validation_error():
    """Test request validation in original assignee search."""
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
        client.patents.search.by_original_assignee()  # Missing application

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_original_assignee(
            application="Test Company",
            limit=2000  # > 1000
        )

    client.close()


def test_current_assignee_search_success():
    """Test successful current assignee search."""
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

    resp = client.patents.search.by_current_assignee(
        assignee="Apple, Inc.",
        limit=50
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
    assert json_data["assignee"] == "Apple, Inc."
    assert json_data["limit"] == 50

    client.close()


def test_current_assignee_search_validation_error():
    """Test request validation in current assignee search."""
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
        client.patents.search.by_current_assignee()  # Missing assignee

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_current_assignee(
            assignee="Test Company",
            limit=2000  # > 1000
        )

    client.close()


def test_defense_patent_search_success():
    """Test successful defense patent search."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "CN123456A",
                    "apdt": 20220301,
                    "apno": "CN202200123456",
                    "pbdt": 20230301,
                    "title": "Advanced Defense Communication System",
                    "inventor": "ZHANG, WEI | LI, MING",
                    "patent_id": "defense-123-456",
                    "current_assignee": "Lockheed Martin Corporation",
                    "original_assignee": "Lockheed Martin Corporation"
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

    resp = client.patents.search.by_defense_applicant(
        application="Lockheed Martin Corporation",
        limit=50
    )

    # Verify response structure
    assert resp.result_count == 1
    assert resp.total_search_result_count == 500
    assert len(resp.results) == 1
    
    # Verify patent data
    patent = resp.results[0]
    assert patent.pn == "CN123456A"
    assert patent.title == "Advanced Defense Communication System"
    assert patent.current_assignee == "Lockheed Martin Corporation"

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["application"] == "Lockheed Martin Corporation"
    assert json_data["limit"] == 50

    client.close()


def test_defense_patent_search_validation_error():
    """Test request validation in defense patent search."""
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
        client.patents.search.by_defense_applicant()  # Missing application

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_defense_applicant(
            application="Test Defense Organization",
            limit=2000  # > 1000
        )

    client.close()


def test_similar_patent_search_by_id():
    """Test successful similar patent search by patent ID."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "JP1999068462A",
                    "apdt": 20211108,
                    "apno": "US17/521392",
                    "pbdt": 20230815,
                    "title": "Techniques for using multiple symbols to provide feedback for a sidelink transmission",
                    "inventor": "ELSHAFIE, AHMED | YANG, WEI | HOSSEINI, SEYEDKIANOUSH",
                    "patent_id": "1a47a70d-6b54-4709-a72a-ed552781fcac",
                    "relevancy": "99%",
                    "current_assignee": "QUALCOMM INCORPORATED",
                    "original_assignee": "QUALCOMM INCORPORATED"
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

    resp = client.patents.search.by_similarity(
        patent_id="b053642f-3108-4ea9-b629-420b0ab959e3",
        limit=50,
        relevancy="70%"
    )

    # Verify response structure
    assert resp.result_count == 1
    assert resp.total_search_result_count == 500
    assert len(resp.results) == 1
    
    # Verify patent data with relevancy
    patent = resp.results[0]
    assert patent.pn == "JP1999068462A"
    assert patent.title == "Techniques for using multiple symbols to provide feedback for a sidelink transmission"
    assert patent.relevancy == "99%"
    assert patent.patent_id == "1a47a70d-6b54-4709-a72a-ed552781fcac"

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["patent_id"] == "b053642f-3108-4ea9-b629-420b0ab959e3"
    assert json_data["limit"] == 50
    assert json_data["relevancy"] == "70%"

    client.close()


def test_similar_patent_search_validation_error():
    """Test request validation in similar patent search."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"results": [], "result_count": 0, "total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing both patent_id and patent_number
    with pytest.raises(ValueError, match="Either patent_id or patent_number must be provided"):
        client.patents.search.by_similarity()

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_similarity(
            patent_id="test-id",
            limit=2000  # > 1000
        )

    client.close()


def test_semantic_search_basic():
    """Test basic semantic search functionality."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "results": [
                {
                    "pn": "CN123456789A",
                    "apdt": 20210301,
                    "apno": "CN202100123456",
                    "pbdt": 20220301,
                    "title": "Automobile Front-View Wireless Video Transmission System",
                    "inventor": "ZHANG, WEI | LI, MING | WANG, LEI",
                    "patent_id": "semantic-test-123",
                    "relevancy": "95%",
                    "current_assignee": "AUTOMOTIVE TECH CORP",
                    "original_assignee": "AUTOMOTIVE TECH CORP"
                }
            ],
            "result_count": 1,
            "total_search_result_count": 250
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test with technical description
    technical_text = """The invention discloses an automobile front-view based wireless video transmission system and method. 
    The system comprises a front-view camera, a wireless video transmitting module, a wireless video receiving module, 
    a display screen, a display triggering device, a first controller, a wireless command transmitting module, 
    a wireless command receiving module, a second controller and an automobile starting detecting module."""

    resp = client.patents.search.by_semantic_text(
        text=technical_text,
        limit=50,
        relevancy="60%"
    )

    # Verify response structure
    assert resp.result_count == 1
    assert resp.total_search_result_count == 250
    assert len(resp.results) == 1
    
    # Verify patent data with relevancy
    patent = resp.results[0]
    assert patent.pn == "CN123456789A"
    assert patent.title == "Automobile Front-View Wireless Video Transmission System"
    assert patent.relevancy == "95%"
    assert patent.patent_id == "semantic-test-123"

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["text"] == technical_text
    assert json_data["limit"] == 50
    assert json_data["relevancy"] == "60%"

    client.close()


def test_semantic_search_validation_errors():
    """Test semantic search parameter validation."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"results": [], "result_count": 0, "total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing text parameter
    with pytest.raises(TypeError):  # Missing required parameter
        client.patents.search.by_semantic_text()

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_semantic_text(
            text="Test text",
            limit=2000  # > 1000
        )

    client.close()


def test_image_upload_success():
    """Test successful image upload."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "url": "https://img1.baidu.com/it/u=3787347995,722716643&fm=26&fmt=auto",
            "expire": 32400
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test with BytesIO object (simulating file upload)
    from io import BytesIO
    
    # Create a mock JPEG file in memory
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00'
    image_file = BytesIO(jpeg_data)
    image_file.name = "test_image.jpg"
    
    resp = client.patents.search.upload_image(image=image_file)

    # Verify response structure
    assert resp.url == "https://img1.baidu.com/it/u=3787347995,722716643&fm=26&fmt=auto"
    assert resp.expire == 32400

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"

    client.close()


def test_image_upload_validation_errors():
    """Test image upload validation errors."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"url": "", "expire": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test invalid image parameter type
    with pytest.raises(ValueError, match="Image must be a file path"):
        client.patents.search.upload_image(image=123)  # Invalid type

    client.close()


def test_image_search_design_patents():
    """Test image search for design patents."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "patent_messages": [
                {
                    "url": "http://example.com/patent_image.png",
                    "apdt": 20190528,
                    "apno": "EU006535076",
                    "pbdt": 20190528,
                    "score": 0.8884816,
                    "title": "Mobile phones",
                    "inventor": "SMITH, JOHN|DOE, JANE",
                    "loc_match": 1,
                    "patent_id": "6e433449-143b-41d9-9abf-6c6519b07779",
                    "patent_pn": "EU0065350760001S",
                    "current_assignee": "HUAWEI TECHNOLOGIES CO., LTD.",
                    "original_assignee": "HUAWEI TECHNOLOGIES CO., LTD."
                }
            ],
            "total_search_result_count": 100
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.patents.search.by_image(
        url="https://example.com/design_image.jpg",
        patent_type="D",
        model=1,  # Smart Recommendation for designs
        limit=50,
        country=["US", "EU", "CN"]
    )

    # Verify response structure
    assert resp.total_search_result_count == 100
    assert len(resp.patent_messages) == 1
    
    # Verify patent data with similarity score
    patent = resp.patent_messages[0]
    assert patent.patent_pn == "EU0065350760001S"
    assert patent.title == "Mobile phones"
    assert patent.score == 0.8884816
    assert patent.loc_match == 1

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["url"] == "https://example.com/design_image.jpg"
    assert json_data["patent_type"] == "D"
    assert json_data["model"] == 1
    assert json_data["limit"] == 50
    assert json_data["country"] == ["US", "EU", "CN"]

    client.close()


def test_image_search_validation_errors():
    """Test image search parameter validation."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"patent_messages": [], "total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing required parameters
    with pytest.raises(TypeError):  # Missing required parameters
        client.patents.search.by_image()

    # Test limit too high
    with pytest.raises(Exception):  # Pydantic validation error
        client.patents.search.by_image(
            url="https://example.com/image.jpg",
            patent_type="D",
            model=1,
            limit=200  # > 100
        )

    client.close()


def test_multi_image_search_design_patents():
    """Test multi-image search for design patents."""
    oauth_payload = create_oauth_payload()
    
    business_payload = {
        "data": {
            "patent_messages": [
                {
                    "url": "http://example.com/multi_patent_image.png",
                    "apdt": 20200315,
                    "apno": "US16987654",
                    "pbdt": 20210315,
                    "score": 0.9234567,
                    "title": "Multi-view Mobile Device Design",
                    "inventor": "BROWN, ALICE|GREEN, BOB",
                    "loc_match": 1,
                    "patent_id": "multi-test-123",
                    "patent_pn": "US11987654B2",
                    "current_assignee": "TECH INNOVATIONS INC",
                    "original_assignee": "TECH INNOVATIONS INC"
                }
            ],
            "total_search_result_count": 85
        },
        "status": True,
        "error_code": 0,
    }

    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    resp = client.patents.search.by_multiple_images(
        urls=[
            "https://example.com/design_front.jpg",
            "https://example.com/design_back.jpg",
            "https://example.com/design_side.jpg"
        ],
        patent_type="D",
        model=1,  # Smart Recommendation for designs
        limit=40,
        country=["US", "EU", "CN"]
    )

    # Verify response structure
    assert resp.total_search_result_count == 85
    assert len(resp.patent_messages) == 1
    
    # Verify patent data with similarity score
    patent = resp.patent_messages[0]
    assert patent.patent_pn == "US11987654B2"
    assert patent.title == "Multi-view Mobile Device Design"
    assert patent.score == 0.9234567
    assert patent.loc_match == 1

    # Verify request details
    assert session.last_request.headers["Authorization"].startswith("Bearer ")
    assert session.last_request.params["apikey"] == "client-id"
    
    # Verify JSON payload
    json_data = session.last_request.json
    assert json_data["urls"] == [
        "https://example.com/design_front.jpg",
        "https://example.com/design_back.jpg", 
        "https://example.com/design_side.jpg"
    ]
    assert json_data["patent_type"] == "D"
    assert json_data["model"] == 1
    assert json_data["limit"] == 40
    assert json_data["country"] == ["US", "EU", "CN"]

    client.close()


def test_multi_image_search_validation_errors():
    """Test multi-image search parameter validation."""
    oauth_payload = create_error_oauth_payload()
    
    business_payload = {
        "status": True, 
        "error_code": 0, 
        "data": {"patent_messages": [], "total_search_result_count": 0}
    }
    
    session = FakeSession(FakeResponse(200, oauth_payload), FakeResponse(200, business_payload))
    client = make_client_with_session(session)

    # Test missing required parameters
    with pytest.raises(TypeError):  # Missing required parameters
        client.patents.search.by_multiple_images()

    # Test empty URLs list
    with pytest.raises(ValueError, match="At least one image URL is required"):
        client.patents.search.by_multiple_images(
            urls=[],
            patent_type="D",
            model=1
        )

    # Test too many URLs (>4)
    with pytest.raises(ValueError, match="Maximum 4 image URLs are allowed"):
        client.patents.search.by_multiple_images(
            urls=[
                "https://example.com/1.jpg",
                "https://example.com/2.jpg",
                "https://example.com/3.jpg",
                "https://example.com/4.jpg",
                "https://example.com/5.jpg"  # 5th image - too many
            ],
            patent_type="D",
            model=1
        )

    client.close()
