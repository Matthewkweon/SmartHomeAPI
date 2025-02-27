# Smart Home API & Structure
## Overview
This project provides a structured system for managing a smart home, including users, houses, rooms, and devices. The system is built using Python and includes object-oriented classes that allow the creation, modification, and deletion of entities within the home. Additionally, unit tests are provided using pytest to ensure system functionality. I tried to make sure that each of the functions were tested individually and fit together as one. You will see that I implemented a sort of heirarchical structure where each class can affect one another. 


## System Structure

The system follows a hierarchical structure:
- Users own houses
- Houses contain rooms
- Rooms contain devices

### Class Overview

1. **User**
   - Represents a homeowner/user in the system
   - Can own multiple houses
   - Attributes: name, username, phone, privileges, email

2. **House**
   - Represents a physical property
   - Belongs to a user
   - Contains multiple rooms
   - Attributes: name, address, GPS coordinates

3. **Room**
   - Represents a room within a house
   - Contains multiple devices
   - Attributes: name, floor, size, room type

4. **Device**
   - Represents a smart device
   - Located in a specific room
   - Attributes: device type, name, settings, data, status

## Project Structure
```python
/smarthome
│── smarthome.py     # Main module containing User, House, Room, and Device classes
│── test_smarthome.py # Pytest unit tests
│── README.md        # Project documentation
```

First, install pytest:
```python
pip install pytest
```

### Usage
Example: Creating Users, Houses, Rooms, and Devices
```python
from smarthome import User, House, Room, Device

# Create a user
user = User(name="Alice", username="alice123", phone="555-1234", privileges="admin", email="alice@mail.com")

# Create a house and assign it to the user
house = House(name="Alice's House", address="123 Main St", gps="40.7128° N, 74.0060° W", owner=user)

# Create a room inside the house
room = Room(name="Living Room", floor=1, size=200, house=house, room_type="Common Area")

# Add a device to the room
device = Device(device_type="thermostat", name="Nest Thermostat", room=room, settings={"temperature": 72}, status="active")

# Print user data as dictionary
print(user.to_dict())
```


#### Output
```python
{
    "name": "Alice",
    "username": "alice123",
    "phone": "555-1234",
    "privileges": "admin",
    "email": "alice@mail.com",
    "houses": [
        {
            "name": "Alice's House",
            "address": "123 Main St",
            "gps": "40.7128° N, 74.0060° W",
            "owner": "alice123",
            "rooms": [
                {
                    "name": "Living Room",
                    "floor": 1,
                    "size": 200,
                    "house": "Alice's House",
                    "room_type": "Common Area",
                    "devices": [
                        {
                            "device_type": "thermostat",
                            "name": "Nest Thermostat",
                            "room": "Living Room",
                            "settings": {
                                "temperature": 72
                            },
                            "data": {},
                            "status": "active"
                        }
                    ]
                }
            ]
        }
    ]
}
```

### Running Tests
Pytest is used to validate the functionality of the system.

Steps to Run Tests:
Navigate to the project directory and run:
```bash
pytest test_smarthome.py -v
```

You can also run your own tests. You just need to make a function within test_smarthome.py and run the command above. 

Expected Output:
```bash
================== test session starts ==================
test_smarthome.py::test_create_blank_user PASSED
test_smarthome.py::test_create_blank_house PASSED
test_smarthome.py::test_create_blank_room PASSED
test_smarthome.py::test_create_blank_device PASSED
...
================== 15 passed in 0.12s ==================
```