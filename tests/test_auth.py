from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={
            "username": "testuser123456",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "message": "Created account for testuser123456"
    }
