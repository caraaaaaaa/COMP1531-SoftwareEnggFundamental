'''
Tests for check_password()
'''
from password import check_password

def test_example():
    assert check_password("12a12A123123") == "Strong password"

    assert check_password("1234567a") == "Moderate password"
    assert check_password("1234567A") == "Moderate password"
    assert check_password("12345678") == "Moderate password"

    assert check_password("ihearttrimesters") == "Poor password"
    assert check_password("abcdefgh") == "Poor password"
    assert check_password("") == "Poor password"

    assert check_password("password") == "Horrible password"
    assert check_password("iloveyou") == "Horrible password"
    assert check_password("123456") == "Horrible password"