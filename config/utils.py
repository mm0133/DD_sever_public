import datetime
import json

from django.http import Http404
from django.shortcuts import _get_queryset
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def HitCountResponse(request, obj, response):
    # [1] 로그인 확인
    if not request.user.is_authenticated:
        cookie_name = 'DDHit'
    else:
        cookie_name = f'DDHit:{request.user.id}'

    # [2] 그 날 당일 밤 12시에 쿠키 삭제
    tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    objName = obj.__class__.__name__
    # [3] hit 를 check 하는 쿠키가 있는 경우
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_dict = json.loads(cookies)
        if objName in cookies_dict:
            if obj.id not in cookies_dict[objName]:
                cookies_dict[objName] = cookies_dict[objName].append(obj.id)
                obj.hitNums += 1
                obj.save()
                returnCookies = json.dumps(cookies_dict)
                response.set_cookie(cookie_name, returnCookies, expires=expires)

        else:
            cookies_dict[objName] = [obj.id]
            obj.hitNums += 1
            obj.save()
            returnCookies = json.dumps(cookies_dict)
            response.set_cookie(cookie_name, returnCookies, expires=expires)

        return response

    # [4] hit 를 check 하는 쿠키가 없는 경우

    cookies_dict = {objName: [obj.id]}
    obj.hitNums += 1
    obj.save()
    returnCookies = json.dumps(cookies_dict)
    response.set_cookie(cookie_name, returnCookies, expires=expires)

    return response


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


def pagination_with_pagesize(pagesize):
    class ReturnClass(PageNumberPagination):
        page_size = pagesize

    return ReturnClass


def notFoundErrorMaker(message):
    class Http404Custom(Exception):
        war



