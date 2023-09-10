def check_if_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def check_if_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


def check_if_positive(number):
    if number > 0:
        return True
    else:
        return False


def check_if_word(word):
    if word.isalpha():
        return True
    else:
        return False


def check_if_phone(phone):
    if len(phone) == 10:
        return True
    else:
        return False
