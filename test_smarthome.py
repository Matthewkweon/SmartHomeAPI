import pytest
from smarthome import User, House, Room, Device  # Adjust this import as necessary

@pytest.fixture(autouse=True)
def cleanup():
    """Ensure each test starts with a fresh state"""
    User.users.clear()
    House.houses.clear()
    Room.rooms.clear()
    Device.devices.clear()


@pytest.fixture
def setup_data():
    """Setup test data for users, houses, rooms, and devices."""
    user = User().create_blank()
    user.name = "Alice"
    user.username = "alice123"
    user.phone = "555-1234"
    user.privileges = "admin"
    user.email = "alice@mail.com"

    house = House().create_blank()
    house.name = "Alice's House"
    house.address = "123 Main St"
    house.gps = "40.7128° N, 74.0060° W"
    house.owner = user
    user.houses.append(house)

    room = Room().create_blank()
    room.name = "Living Room"
    room.floor = 1
    room.size = 200
    room.house = house
    house.rooms.append(room)

    device = Device().create_blank()
    device.device_type = "thermostat"
    device.name = "Nest Thermostat"
    device.room = room
    device.settings = {"temperature": 72}
    device.data = {"last_update": "2025-02-12"}
    device.status = "active"
    room.devices.append(device)

    return user, house, room, device


def test_create_blank_user():
    print(len(User.users))

    user = User().create_blank()
    print(len(User.users))
    assert user.name == ""
    assert user.username == ""
    assert user.phone == ""
    assert user.privileges == ""
    assert user.email == ""


def test_create_blank_house():
    house = House().create_blank()
    assert house.name == ""
    assert house.address == ""
    assert house.gps == ""


def test_create_blank_room():
    room = Room().create_blank()
    assert room.name == ""
    assert room.floor == 0
    assert room.size == 0
    assert room.room_type == ""


def test_create_blank_device():
    device = Device().create_blank()
    assert device.device_type == ""
    assert device.name == ""
    assert device.settings == {}
    assert device.data == {}
    assert device.status == ""


def test_add_house_to_user(setup_data):
    user, house, _, _ = setup_data
    assert len(user.houses) == 1
    assert user.houses[0].name == "Alice's House"


def test_add_room_to_house(setup_data):
    _, house, room, _ = setup_data
    assert len(house.rooms) == 1
    assert house.rooms[0].name == "Living Room"


def test_add_device_to_room(setup_data):
    _, _, room, device = setup_data
    assert len(room.devices) == 1
    assert room.devices[0].name == "Nest Thermostat"


def test_update_user(setup_data):
    user, _, _, _ = setup_data
    user.name = "Bob"
    assert user.name == "Bob"


def test_update_house(setup_data):
    _, house, _, _ = setup_data
    house.address = "456 Elm St"
    assert house.address == "456 Elm St"


def test_update_room(setup_data):
    _, _, room, _ = setup_data
    room.size = 300
    assert room.size == 300


def test_update_device(setup_data):
    _, _, _, device = setup_data
    device.status = "inactive"
    assert device.status == "inactive"


def test_delete_device(setup_data):
    _, _, room, device = setup_data
    device.delete()
    assert len(room.devices) == 0


def test_delete_room(setup_data):
    _, house, room, _ = setup_data
    room.delete()
    assert len(house.rooms) == 0


def test_delete_house(setup_data):
    user, house, _, _ = setup_data
    house.delete()
    assert len(user.houses) == 0


def test_create_blank_user():
    print("Before Creating Blank User:", len(User.users))
    user = User().create_blank()
    print("After Creating Blank User:", len(User.users))
    assert len(User.users) == 1  # Should be 1 now

def test_delete_user(setup_data):
    user, _, _, _ = setup_data

    print("\nBefore Delete:", len(User.users), User.users)

    user.delete()

    print("After Delete:", len(User.users), User.users)  # Should be 0 now

    assert len(User.users) == 0
