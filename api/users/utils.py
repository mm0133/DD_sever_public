def validate_phoneNumber(phoneNumber):
    if (not phoneNumber.isdigit) \
            or len(phoneNumber) != 11 \
            or phoneNumber[0:2] != '01':
        return False
    else:
        return True


from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

