class User:
    users = []

    def __init__(self, name="", username="", phone="", privileges="", email=""):
        self.name = name
        self.username = username
        self.phone = phone
        self.privileges = privileges
        self.email = email
        self.houses = []
        try:
            User.users.append(self)
        except:
            ValueError("User already exists.")

    @classmethod
    def create_blank(cls):
        for user in cls.users[:]:  # Create a copy of the list to iterate
            if (user.name == "" and user.username == "" and 
                user.phone == "" and user.privileges == "" and 
                user.email == "" and not user.houses):
                cls.users.remove(user)
        
        user = cls()  # This will add it to users list via __init__
        return user

    def delete(self):
        print(f"Deleting User: {self.username}")

        # Ensure all houses are deleted
        while len(self.houses) > 0:
            house = self.houses.pop()
            print(f"Deleting House: {house.name}")
            house.delete()

        # Remove from users list
        if self in User.users:
            User.users.remove(self)
            print(f"User {self.username} removed successfully!")

        print("Final User List After Deletion:", User.users)


    def update(self, name, username, phone, privileges, email):
        try:
            self.name = name
            self.username = username
            self.phone = phone
            self.privileges = privileges
            self.email = email
            return f"User {self.username} updated successfully!"
        except:
            return ValueError("User update failed.")

    def to_dict(self):
        try:
            return {
                "name": self.name,
                "username": self.username,
                "phone": self.phone,
                "privileges": self.privileges,
                "email": self.email,
                "houses": [house.to_dict() for house in self.houses]
            }
        except:
            return ValueError("User to_dict failed.")

class House:
    houses = []

    def __init__(self, name="", address="", gps="", owner=None):
        self.name = name
        self.address = address
        self.gps = gps
        self.owner = owner
        self.rooms = []
        if owner:
            owner.houses.append(self)
        else:
            ValueError("House must have an owner.")
        House.houses.append(self)

    def create_blank(self):
        return House()

    def delete(self):
        while self.rooms:
            self.rooms[0].delete()

        if self.owner and self in self.owner.houses:
            self.owner.houses.remove(self)  # FIX: Only remove if it exists

        House.houses.remove(self)

    def update(self, name, address, gps, owner):
        try:
            self.name = name
            self.address = address
            self.gps = gps
            self.owner = owner
            message = f"House {self.name} updated successfully!"
            return message
        except:
            return ValueError("House update failed.")


    def to_dict(self):
        try:
            return {
                "name": self.name,
                "address": self.address,
                "gps": self.gps,
                "owner": self.owner.username if self.owner else None,  # FIX: Store only username, not full object
                "rooms": [room.to_dict() for room in self.rooms]
            }
        except:
            return ValueError("House to_dict failed.")



class Room:
    rooms = []

    def __init__(self, name="", floor=0, size=0, house=None, room_type=""):
        self.name = name
        self.floor = floor
        self.size = size
        self.house = house
        self.devices = []
        self.room_type = room_type
        if house:
            house.rooms.append(self)
        Room.rooms.append(self)

    def create_blank(self):
        return Room()

    def delete(self):
        """Delete all devices before removing room from house."""
        while self.devices:
            self.devices[0].delete()
        if self.house:
            self.house.rooms.remove(self)
        Room.rooms.remove(self)
    def update(self, name, floor, size, house, room_type):
        try:
            self.name = name
            self.floor = floor
            self.size = size
            self.house = house
            self.room_type = room_type
            message = f"Room {self.name} updated successfully!"
            return message
        except:
            return ValueError("Room update failed.")

    def to_dict(self):
        try:
            return {
                "name": self.name,
                "floor": self.floor,
                "size": self.size,
                "house": self.house.name if self.house else None,  # FIX: Store house name, not full object
                "room_type": self.room_type,
                "devices": [device.to_dict() for device in self.devices]
            }
        except:
            return ValueError("Room to_dict failed.")




class Device:
    devices = []

    def __init__(self, device_type="", name="", room=None, settings=None, data=None, status=""):
        self.device_type = device_type
        self.name = name
        self.room = room
        self.settings = settings if settings else {}
        self.data = data if data else {}
        self.status = status
        if room:
            room.devices.append(self)
        Device.devices.append(self)

    def create_blank(self):
        return Device()

    def delete(self):
        """Remove device from its associated room."""
        if self.room:
            self.room.devices.remove(self)
        Device.devices.remove(self)

    def update(self, device_type, name, room, settings, data, status):
        try:
            self.device_type = device_type
            self.name = name
            self.room = room
            self.settings = settings
            self.data = data
            self.status = status
            message = f"Device {self.name} updated successfully!"
            return message
        except:
            return ValueError("Device update failed.")

    def to_dict(self):
        try:
            return {
                "device_type": self.device_type,
                "name": self.name,
                "settings": self.settings,
                "data": self.data,
                "status": self.status
            }
        except:
            return ValueError("Device to_dict failed.")

