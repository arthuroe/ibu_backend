import re


def validate_email(email):
    if re.search('[^@]+@[^@]+\.[^@]+', email):
        return True
    return False
