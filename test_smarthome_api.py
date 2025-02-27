import pytest
from fastapi.testclient import TestClient
from smarthome_api import app

# Create a TestClient instance using our FastAPI app
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    """
    This fixture runs before each test. 
    Since your classes hold data in in-memory lists (e.g., User.users),
    we can 'reset' them by re-importing them or by explicitly clearing them 
    if you have a cleanup endpoint in your app.

    Alternatively, if you rely on the class-level lists in smartphone.py,
    you can add an endpoint to reset data for test purposes,
    or manually clear them here if you have direct import access.
    For demonstration, I'll do a 'best effort' approach by calling 
    all delete endpoints for each resource we might have created.
    """
    # Attempt to delete all users, houses, rooms, devices
    # in reverse order (devices->rooms->houses->users)
    # so references don't break.
    # The below approach queries each endpoint and deletes resources by name.
    # If your code changes, update accordingly.

    # Delete all devices:
    r = client.get("/devices")
    if r.status_code == 200:
        for device in r.json():
            name = device["name"]
            client.delete(f"/devices/{name}")

    # Delete all rooms:
    r = client.get("/rooms")
    if r.status_code == 200:
        for room in r.json():
            name = room["name"]
            client.delete(f"/rooms/{name}")

    # Delete all houses:
    r = client.get("/houses")
    if r.status_code == 200:
        for house in r.json():
            name = house["name"]
            client.delete(f"/houses/{name}")

    # Delete all users:
    r = client.get("/users")
    if r.status_code == 200:
        for user in r.json():
            username = user["username"]
            client.delete(f"/users/{username}")


def test_create_user():
    """
    Test creating a new User via /users POST.
    """
    user_data = {
        "name": "John Doe",
        "username": "johnny",
        "phone": "555-1234",
        "privileges": "admin",
        "email": "johnny@example.com"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "johnny"
    assert data["name"] == "John Doe"


def test_get_all_users():
    """
    Test retrieving all users via GET /users.
    """
    # First, create a user
    client.post("/users", json={
        "name": "Alice",
        "username": "alice123",
        "phone": "555-9999",
        "privileges": "user",
        "email": "alice@mail.com"
    })
    # Now get all users
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["username"] == "alice123"


def test_create_house():
    """
    Test creating a new House via /houses POST.
    Must have a user to own the house.
    """
    # Create user first
    client.post("/users", json={
        "name": "Alice",
        "username": "alice123",
        "phone": "555-9999",
        "privileges": "user",
        "email": "alice@mail.com"
    })
    # Create house
    house_data = {
        "name": "Beach House",
        "address": "123 Ocean Drive",
        "gps": "25.774, -80.196",
        "owner_username": "alice123"
    }
    response = client.post("/houses", json=house_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Beach House"
    assert data["owner"] == "alice123"


def test_create_room():
    """
    Test creating a new Room via /rooms POST.
    Must have a House to place the Room.
    """
    # Create user
    client.post("/users", json={
        "name": "Alice",
        "username": "alice123",
        "phone": "555-9999",
        "privileges": "user",
        "email": "alice@mail.com"
    })
    # Create house
    client.post("/houses", json={
        "name": "Beach House",
        "address": "123 Ocean Drive",
        "gps": "25.774, -80.196",
        "owner_username": "alice123"
    })
    # Create room
    room_data = {
        "name": "Living Room",
        "floor": 1,
        "size": 300,
        "house_name": "Beach House",
        "room_type": "Common"
    }
    response = client.post("/rooms", json=room_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Living Room"
    assert data["house"] == "Beach House"


def test_create_device():
    """
    Test creating a new Device via /devices POST.
    Must have a Room to place the Device.
    """
    # Create user
    client.post("/users", json={
        "name": "Alice",
        "username": "alice123",
        "phone": "555-9999",
        "privileges": "user",
        "email": "alice@mail.com"
    })
    # Create house
    client.post("/houses", json={
        "name": "Beach House",
        "address": "123 Ocean Drive",
        "gps": "25.774, -80.196",
        "owner_username": "alice123"
    })
    # Create room
    client.post("/rooms", json={
        "name": "Living Room",
        "floor": 1,
        "size": 300,
        "house_name": "Beach House",
        "room_type": "Common"
    })
    # Create device
    device_data = {
        "device_type": "thermostat",
        "name": "Nest Thermostat",
        "settings": {"temperatureUnit": "Fahrenheit"},
        "data": {"currentTemp": 70},
        "status": "on",
        "room_name": "Living Room"
    }
    response = client.post("/devices", json=device_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Nest Thermostat"
    assert data["settings"]["temperatureUnit"] == "Fahrenheit"


def test_update_user():
    """
    Test updating a user via PUT /users/{username}.
    """
    # Create user
    client.post("/users", json={
        "name": "Alice",
        "username": "alice123",
        "phone": "555-9999",
        "privileges": "user",
        "email": "alice@mail.com"
    })
    # Update user
    update_data = {"phone": "555-0000", "privileges": "admin"}
    response = client.put("/users/alice123", json=update_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["phone"] == "555-0000"
    assert updated_user["privileges"] == "admin"


def test_delete_user():
    """
    Test deleting a user via DELETE /users/{username}.
    """
    # Create user
    client.post("/users", json={
        "name": "Alice",
        "username": "alice123",
        "phone": "555-9999",
        "privileges": "user",
        "email": "alice@mail.com"
    })
    # Delete user
    response = client.delete("/users/alice123")
    assert response.status_code == 200
    # Confirm user is gone
    get_response = client.get("/users/alice123")
    assert get_response.status_code == 404
