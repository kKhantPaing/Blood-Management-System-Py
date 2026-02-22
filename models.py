class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password


class Donor(User):
    def __init__(self,  name, phone, address, blood_type):
        self.name = name
        self.phone = phone
        self.address = address
        self.blood_type = blood_type
    
    
class BloodType:
    def __init__(self, blood_type, rh, description):
        self.blood_type = blood_type
        self.rh = rh
        self.description = description

