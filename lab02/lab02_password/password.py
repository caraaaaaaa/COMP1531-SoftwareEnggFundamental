def check_password(password):
    '''
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    '''
    number = any(char.isdigit() for char in password)
    upper = any(char.isupper() for char in password)
    lower = any(char.islower() for char in password)
    horrible = ["password", "iloveyou", "123456"]
    if len(password) >= 12 and number and upper and lower:
        return "Strong password"
    elif len(password) >= 8 and number:
        return "Moderate password"
    elif password in horrible:
        return "Horrible password"
    else:
        return "Poor password"
    #pass

if __name__ == '__main__':
    print(check_password("ihearttrimesters"))
    # What does this do?
