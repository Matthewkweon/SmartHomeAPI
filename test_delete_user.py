import pytest
from smarthome import User, House, Room, Device  # Adjust import if needed

@pytest.fixture(autouse=True)
def cleanup():
    """Ensure each test starts with a fresh state"""
    print("\nBefore Cleanup: Users =", len(User.users))
    User.users.clear()
    House.houses.clear()
    Room.rooms.clear()
    Device.devices.clear()
    print("After Cleanup: Users =", len(User.users))

@pytest.fixture
def setup_data():
    """Setup test user."""
    user = User().create_blank()
    user.name = "Alice"
    user.username = "alice123"
    user.phone = "555-1234"
    user.privileges = "admin"
    user.email = "alice@mail.com"
    
    print("\nUser Created:", user.to_dict())
    return user

def test_delete_user(setup_data):
    user = setup_data
    print("\nBefore Delete: Users =", len(User.users), User.users)
    
    user.delete()
    
    print("After Delete: Users =", len(User.users), User.users)
    
    assert len(User.users) == 0
