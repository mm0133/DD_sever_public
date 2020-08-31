def validate_phoneNumber(phoneNumber):
    if (not phoneNumber.isdigit) \
            or len(phoneNumber) != 11 \
            or phoneNumber[0:2] != '01':
        return False
    else:
        return True
