""" for utility functions like password hashing, etc. """
import hashlib as hl


def hash_password(password):
    """ Hash a password using SHA-256 """
    return hl.sha256(password.encode()).hexdigest()
