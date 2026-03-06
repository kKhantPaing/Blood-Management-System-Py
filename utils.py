""" for utility functions like password hashing, etc. """
import hashlib as hl


def hash_password(password):
    """ Hash a password using SHA-256 """
    return hl.sha256(password.encode()).hexdigest()


def is_strong_password(password):
    """ Check if a password is strong enough """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
