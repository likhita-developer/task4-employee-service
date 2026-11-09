from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_employee_not_found():
    response = client.get("/employees/UnknownEmployee123")
    assert response.status_code == 404


def test_create_employee():
    response = client.post(
        "/employees",
        json={"name": "Test Employee", "department": "IT", "salary": 50000},
    )

    if response.status_code == 400:
        assert response.json()["detail"] == "Employee already exists"
    else:
        assert response.status_code == 200
        assert response.json()["name"] == "Test Employee"


def test_empty_name():
    response = client.post(
        "/employees", json={"name": "", "department": "IT", "salary": 50000}
    )
    assert response.status_code == 422


def test_invalid_salary():
    response = client.post(
        "/employees",
        json={"name": "Invalid Salary Test", "department": "IT", "salary": -100},
    )
    assert response.status_code == 422
