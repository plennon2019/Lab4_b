import pytest

def user_payload(name="Paul", email="paul@atu.ie", age=25, student_id="S1234567"):
    return {"name" : name,
            "email" : email,
            "age" : age,
            "student_id" : student_id}


def test_create_user_returns_201(client):
    response = client.post("/api/users", json= user_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1

def test_duplicate_user_id_returns_409(client):
    client.post("/api/users", json=user_payload())

    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()

@pytest.mark.parametrize("bad_student_id", ["123456", "s1234567", "S123", "S12345678"])

def test_bad_student_return_422(client, bad_student_id):
    response = client.post("/api/users", json=user_payload(student_id=bad_student_id))
    assert response.status_code ==422

def test_get_users_returns_created_users(client):
    client.post("/api/users", json=user_payload(name="Paul", email="pal@atu.ie", student_id="S2234567"))
    client.post("/api/users", json=user_payload(name="Paul", email="paul@atu.ie"))

    response = client.get("/api/users")
    user_data = response.json()[1]["id"]
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["id"] == user_data
    assert data[0]["name"] == "Paul"

def test_get_existing_users_returns_200(client):
    data =client.post("/api/users", json=user_payload())
    user_id = data.json()["id"]
    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id

