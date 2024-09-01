import re


def check_username_and_password_format(type_un_or_pw, username_or_password):
    if type_un_or_pw == 'username':
        pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{5,}$'
        if re.match(pattern, username_or_password):
            return True
        return False
    else:
        pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$'
        if re.match(pattern, username_or_password):
            return True
        return False



