import re


def check_username_and_password_format(type_un_or_pw, username_or_password):
    if type_un_or_pw == 'username':
        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{5,}$'
        if re.match(pattern, username_or_password):
            return True
        return False
    else:
        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$'
        if re.match(pattern, username_or_password):
            return True
        return False


def check_time_format(time):
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern,time ):
        return True
    return False



