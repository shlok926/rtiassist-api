import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base, get_db
from models.schemas import CaseCreate
from main import app

# Setup Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rtiassist.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def test_create_case():
    response = client.post(
        "/cases",
        json={"problem_description": "My problem", "title": "Test Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["problem_description"] == "My problem"
    assert data["title"] == "Test Title"
    assert data["status"] == "UNDERSTANDING"
    assert "id" in data
    
    # Check if CASE_CREATED event was generated
    events = data.get("events")
    assert events is not None
    assert len(events) == 1
    assert events[0]["event_type"] == "CASE_CREATED"

def test_get_case():
    create_response = client.post(
        "/cases",
        json={"problem_description": "Get test"}
    )
    case_id = create_response.json()["id"]

    get_response = client.get(f"/cases/{case_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == case_id
    assert get_response.json()["problem_description"] == "Get test"

def test_list_cases():
    client.post("/cases", json={"problem_description": "List test 1"})
    client.post("/cases", json={"problem_description": "List test 2"})

    response = client.get("/cases")
    assert response.status_code == 200
    data = response.json()
    assert "cases" in data
    assert data["total"] >= 2
    assert len(data["cases"]) >= 2

def test_update_case():
    create_response = client.post(
        "/cases",
        json={"problem_description": "Update test"}
    )
    case_id = create_response.json()["id"]

    update_response = client.patch(
        f"/cases/{case_id}",
        json={"status": "READY_TO_FILE", "title": "Updated Title"}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "READY_TO_FILE"
    assert updated_data["title"] == "Updated Title"

    # Verify event was added
    events = updated_data.get("events")
    assert len(events) == 2
    assert any(e["event_type"] == "STATUS_CHANGED" for e in events)

def test_invalid_status_update():
    create_response = client.post("/cases", json={"problem_description": "Status test"})
    case_id = create_response.json()["id"]

    update_response = client.patch(
        f"/cases/{case_id}",
        json={"status": "INVALID_STATUS"}
    )
    assert update_response.status_code == 400
    assert "Invalid status" in update_response.json()["detail"]

def test_import_legacy_tracker():
    legacy_data = {
        "id": "12345",
        "date": "2023-01-01",
        "department": "Transport Dept",
        "description": "DL renewal",
        "status": "pending"
    }
    response = client.post("/cases/import", json=legacy_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "READY_TO_FILE" # Mapped from pending
    assert data["problem_description"] == "DL renewal"
    assert data["title"] == "Transport Dept"
    
    events = data.get("events")
    assert len(events) == 1
    assert events[0]["event_type"] == "CASE_IMPORTED"
    import json
    metadata = json.loads(events[0]["metadata_json"])
    assert metadata["legacy_id"] == "12345"
