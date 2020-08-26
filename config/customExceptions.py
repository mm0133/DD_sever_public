from django.shortcuts import _get_queryset
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
        raise DDCustomException(f"다음 필수항목이 제출되지 않았습니다: {key}")


def get_object_or_404_custom(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
    if not hasattr(queryset, 'get'):
        raise DDCustomException(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except:
        raise DDCustomException(f"{kwargs}를 만족하는 {klass__name} 객체가 없습니다.", status_code=status.HTTP_404_NOT_FOUND)
