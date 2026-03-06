import pytest
from db_operations import insert_user, login_user
from utils import is_strong_password
from models import User


class TestPasswordStrength:
    """ Test class for password strength validation """

    def test_is_strong_password_valid(self):
        """ Test that a strong password is correctly identified as valid """
        assert is_strong_password("StrongPass1") is True

    def test_is_strong_password_invalid(self):
        """ Test that a weak password is correctly identified as invalid """
        assert is_strong_password("weak") is False
        assert is_strong_password("NoDigits") is False
        assert is_strong_password("nouppercase1") is False
        assert is_strong_password("NOLOWERCASE1") is False
