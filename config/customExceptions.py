from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class DDCustomException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


def get_value_or_error(dictionary, key):
    if dictionary.get(key):
        return dictionary.get(key)
    else:
        raise DDCustomException(f"There is no {key} in request.data")
