import pytest
from employee_api import EmployeeApi

@pytest.fixture(scope="module")
def api():
    return EmployeeApi()

@pytest.fixture
def employee_id(api):
    data = {
        "first_name": "Rick",
        "last_name": "Sanchez",
        "middle_name": "C-137",
        "company_id": 1,
        "email": "rick.sanchez@example.com",
        "phone": "+123456789",
        "birthdate": "1970-01-01",
        "is_active": True
    }
    response = api.create_employee(data)
    assert response.status_code == 200
    return response.json()["id"]

def test_get_employee_info(api, employee_id):
    response = api.get_employee_info(employee_id)
    print("GET response:", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Rick"
    assert data["last_name"] == "Sanchez"

def test_update_employee(api, employee_id):
    updated_data = {
        "phone": "+987654321",
        "is_active": False
    }
    response = api.update_employee(employee_id, updated_data)
    print("UPDATE response:", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+987654321"
    assert data["is_active"] is False
