class User:
    """ User model representing a user in the system """
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password


class Donor:
    """ Donor model representing a blood donor in the system """
    def __init__(
        self,
        donor_id,
        name,
        phone,
        address,
        dob,
        gender,
        blood_type,
        last_donation_date=None,
        is_urgent_available=True,
        is_deleted=False,
    ):
        self.donor_id = donor_id
        self.name = name
        self.phone = phone
        self.address = address
        self.dob = dob
        self.gender = gender
        self.blood_type = blood_type
        self.is_urgent_available = is_urgent_available
        self.last_donation_date = last_donation_date
        self.is_deleted = is_deleted


class BloodDonation:
    """ BloodDonation model representing a blood donation record in the system """
    def __init__(self, donor_id, blood_type, units, donation_date, expiration_date):
        self.donor_id = donor_id
        self.blood_type = blood_type
        self.units = units
        self.donation_date = donation_date
        self.expiration_date = expiration_date
