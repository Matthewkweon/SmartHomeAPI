from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Import your classes from smartphone.py
from smarthome import User, House, Room, Device

app = FastAPI()

# -----------------------------------
# Pydantic Models (Request Schemas)
# -----------------------------------

class UserCreate(BaseModel):
    name: str
    username: str
    phone: str
    privileges: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    privileges: Optional[str] = None
    email: Optional[str] = None

class HouseCreate(BaseModel):
    name: str
    address: str
    gps: str
    owner_username: str

class HouseUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    gps: Optional[str] = None
    owner_username: Optional[str] = None

class RoomCreate(BaseModel):
    name: str
    floor: int
    size: int
    house_name: str
    room_type: str

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    floor: Optional[int] = None
    size: Optional[int] = None
    house_name: Optional[str] = None
    room_type: Optional[str] = None

class DeviceCreate(BaseModel):
    device_type: str
    name: str
    settings: Dict[str, Any] = {}
    data: Dict[str, Any] = {}
    status: str
    room_name: str

class DeviceUpdate(BaseModel):
    device_type: Optional[str] = None
    name: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    room_name: Optional[str] = None


# =========================================
#                USER ROUTES
# =========================================

@app.get("/users", response_model=List[Dict[str, Any]])
def get_all_users():
    """Return a list of all users."""
    return [u.to_dict() for u in User.users]

@app.get("/users/{username}", response_model=Dict[str, Any])
def get_user(username: str):
    """Return a single user by username."""
    user = _find_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.to_dict()

@app.post("/users", response_model=Dict[str, Any])
def create_user(user_data: UserCreate):
    """Create a new user and return the created user."""
    # Check if a user with the same username already exists
    if _find_user_by_username(user_data.username) is not None:
        raise HTTPException(status_code=400, detail="Username already exists.")
    new_user = User(
        name=user_data.name,
        username=user_data.username,
        phone=user_data.phone,
        privileges=user_data.privileges,
        email=user_data.email,
    )
    return new_user.to_dict()

@app.put("/users/{username}", response_model=Dict[str, Any])
def update_user(username: str, user_data: UserUpdate):
    """Update a user's information."""
    user = _find_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Only update fields that are provided (non-None)
    updated_name = user_data.name if user_data.name is not None else user.name
    updated_username = user_data.username if user_data.username is not None else user.username
    updated_phone = user_data.phone if user_data.phone is not None else user.phone
    updated_privileges = user_data.privileges if user_data.privileges is not None else user.privileges
    updated_email = user_data.email if user_data.email is not None else user.email

    # Check if we changed username and if the new username is taken
    if updated_username != user.username and _find_user_by_username(updated_username):
        raise HTTPException(status_code=400, detail="Updated username already exists.")

    user.update(
        updated_name,
        updated_username,
        updated_phone,
        updated_privileges,
        updated_email,
    )
    return user.to_dict()

@app.delete("/users/{username}", response_model=dict)
def delete_user(username: str):
    """Delete a user."""
    user = _find_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.delete()
    return {"message": f"User '{username}' deleted successfully."}


# =========================================
#               HOUSE ROUTES
# =========================================

@app.get("/houses", response_model=List[Dict[str, Any]])
def get_all_houses():
    """Return a list of all houses."""
    return [h.to_dict() for h in House.houses]

@app.get("/houses/{house_name}", response_model=Dict[str, Any])
def get_house(house_name: str):
    """Return a single house by house name."""
    house = _find_house_by_name(house_name)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found.")
    return house.to_dict()

@app.post("/houses", response_model=Dict[str, Any])
def create_house(house_data: HouseCreate):
    """Create a new house."""
    # Check if house with the same name exists
    if _find_house_by_name(house_data.name):
        raise HTTPException(status_code=400, detail="House with this name already exists.")

    owner = _find_user_by_username(house_data.owner_username)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner user not found.")

    new_house = House(
        name=house_data.name,
        address=house_data.address,
        gps=house_data.gps,
        owner=owner,
    )
    return new_house.to_dict()

@app.put("/houses/{house_name}", response_model=Dict[str, Any])
def update_house(house_name: str, house_data: HouseUpdate):
    """Update a house's information."""
    house = _find_house_by_name(house_name)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found.")

    # Only update fields that are provided (non-None)
    new_name = house_data.name if house_data.name is not None else house.name
    new_address = house_data.address if house_data.address is not None else house.address
    new_gps = house_data.gps if house_data.gps is not None else house.gps

    if new_name != house.name and _find_house_by_name(new_name):
        raise HTTPException(status_code=400, detail="Another house already has that name.")

    if house_data.owner_username is not None:
        new_owner = _find_user_by_username(house_data.owner_username)
        if new_owner is None:
            raise HTTPException(status_code=404, detail="New owner user not found.")
    else:
        new_owner = house.owner

    house.update(new_name, new_address, new_gps, new_owner)
    return house.to_dict()

@app.delete("/houses/{house_name}", response_model=dict)
def delete_house(house_name: str):
    """Delete a house."""
    house = _find_house_by_name(house_name)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found.")
    house.delete()
    return {"message": f"House '{house_name}' deleted successfully."}


# =========================================
#               ROOM ROUTES
# =========================================

@app.get("/rooms", response_model=List[Dict[str, Any]])
def get_all_rooms():
    """Return a list of all rooms."""
    return [r.to_dict() for r in Room.rooms]

@app.get("/rooms/{room_name}", response_model=Dict[str, Any])
def get_room(room_name: str):
    """Return a single room by name."""
    room = _find_room_by_name(room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found.")
    return room.to_dict()

@app.post("/rooms", response_model=Dict[str, Any])
def create_room(room_data: RoomCreate):
    """Create a new room."""
    # Check if a room with the same name already exists
    if _find_room_by_name(room_data.name):
        raise HTTPException(status_code=400, detail="Room with this name already exists.")

    house = _find_house_by_name(room_data.house_name)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found for this room.")

    new_room = Room(
        name=room_data.name,
        floor=room_data.floor,
        size=room_data.size,
        house=house,
        room_type=room_data.room_type,
    )
    return new_room.to_dict()

@app.put("/rooms/{room_name}", response_model=Dict[str, Any])
def update_room(room_name: str, room_data: RoomUpdate):
    """Update room details."""
    room = _find_room_by_name(room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found.")

    new_name = room_data.name if room_data.name is not None else room.name
    new_floor = room_data.floor if room_data.floor is not None else room.floor
    new_size = room_data.size if room_data.size is not None else room.size
    new_room_type = room_data.room_type if room_data.room_type is not None else room.room_type

    if new_name != room.name and _find_room_by_name(new_name):
        raise HTTPException(status_code=400, detail="Another room already has that name.")

    if room_data.house_name is not None:
        new_house = _find_house_by_name(room_data.house_name)
        if new_house is None:
            raise HTTPException(status_code=404, detail="New house not found.")
    else:
        new_house = room.house

    room.update(new_name, new_floor, new_size, new_house, new_room_type)
    return room.to_dict()

@app.delete("/rooms/{room_name}", response_model=dict)
def delete_room(room_name: str):
    """Delete a room."""
    room = _find_room_by_name(room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found.")
    room.delete()
    return {"message": f"Room '{room_name}' deleted successfully."}


# =========================================
#              DEVICE ROUTES
# =========================================

@app.get("/devices", response_model=List[Dict[str, Any]])
def get_all_devices():
    """Return a list of all devices."""
    return [d.to_dict() for d in Device.devices]

@app.get("/devices/{device_name}", response_model=Dict[str, Any])
def get_device(device_name: str):
    """Return a single device by name."""
    device = _find_device_by_name(device_name)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found.")
    return device.to_dict()

@app.post("/devices", response_model=Dict[str, Any])
def create_device(device_data: DeviceCreate):
    """Create a new device."""
    # Check if device with the same name already exists
    if _find_device_by_name(device_data.name):
        raise HTTPException(status_code=400, detail="Device with this name already exists.")

    room = _find_room_by_name(device_data.room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found for this device.")

    new_device = Device(
        device_type=device_data.device_type,
        name=device_data.name,
        room=room,
        settings=device_data.settings,
        data=device_data.data,
        status=device_data.status,
    )
    return new_device.to_dict()

@app.put("/devices/{device_name}", response_model=Dict[str, Any])
def update_device(device_name: str, device_data: DeviceUpdate):
    """Update device details."""
    device = _find_device_by_name(device_name)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found.")

    new_device_type = device_data.device_type if device_data.device_type is not None else device.device_type
    new_name = device_data.name if device_data.name is not None else device.name
    new_settings = device_data.settings if device_data.settings is not None else device.settings
    new_data = device_data.data if device_data.data is not None else device.data
    new_status = device_data.status if device_data.status is not None else device.status

    if new_name != device.name and _find_device_by_name(new_name):
        raise HTTPException(status_code=400, detail="Another device with that name already exists.")

    if device_data.room_name is not None:
        new_room = _find_room_by_name(device_data.room_name)
        if new_room is None:
            raise HTTPException(status_code=404, detail="New room not found.")
    else:
        new_room = device.room

    device.update(new_device_type, new_name, new_room, new_settings, new_data, new_status)
    return device.to_dict()

@app.delete("/devices/{device_name}", response_model=dict)
def delete_device(device_name: str):
    """Delete a device."""
    device = _find_device_by_name(device_name)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found.")
    device.delete()
    return {"message": f"Device '{device_name}' deleted successfully."}


# =========================================
#       HELPER FUNCTIONS (Lookups)
# =========================================

def _find_user_by_username(username: str) -> Optional[User]:
    return next((u for u in User.users if u.username == username), None)

def _find_house_by_name(name: str) -> Optional[House]:
    return next((h for h in House.houses if h.name == name), None)

def _find_room_by_name(name: str) -> Optional[Room]:
    return next((r for r in Room.rooms if r.name == name), None)

def _find_device_by_name(name: str) -> Optional[Device]:
    return next((d for d in Device.devices if d.name == name), None)
