import requests

class EmployeeApi:
    BASE_URL = "http://5.101.50.27:8000"

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        response = requests.post(
            f"{self.BASE_URL}/auth/login",
            json={"username": "harrypotter", "password": "expelliarmus"}
        )
        assert response.status_code == 200, "Error, while getting a token"
        return response.json()["user_token"]

    def create_employee(self, data):
        return requests.post(f"{self.BASE_URL}/employee/create", json=data)

    def get_employee_info(self, employee_id):
        return requests.get(f"{self.BASE_URL}/employee/info/{employee_id}")

    def update_employee(self, employee_id, data):
        return requests.patch(
            f"{self.BASE_URL}/employee/change/{employee_id}",
            params={"client_token": self.token},
            json=data
        )
