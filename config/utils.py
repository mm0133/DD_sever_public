import datetime
import json


def hitCountRespose(request, object, response):

    # [1] 로그인 확인
    if not request.user.is_authenticated:
        cookie_name = 'DDhit'
    else:
        cookie_name = f'DDhit:{request.user.id}'

    # [2] 그 날 당일 밤 12시에 쿠키 삭제
    tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    objName = object.__class__.__name__
    # [3] hit를 check하는 쿠키가 있는 경우
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_dict = json.loads(cookies)
        if objName in cookies_dict:
            if not object.id in cookies_dict[objName]:
                cookies_dict[objName]=cookies_dict[objName].append(object.id)
                object.hitNums += 1
                object.save()
                returnCookies = json.dumps(cookies_dict)
                response.set_cookie(cookie_name, returnCookies, expires=expires)

        else:
            cookies_dict[objName]=[object.id]
            object.hitNums += 1
            object.save()
            returnCookies = json.dumps(cookies_dict)
            response.set_cookie(cookie_name, returnCookies, expires=expires)
        return response


    # [4] hit를 check하는 쿠키가 없는 경우

    cookies_dict={objName:object.id}
    object.hitNums += 1
    object.save()
    returnCookies = json.dumps(cookies_dict)
    response.set_cookie(cookie_name, returnCookies, expires=expires)

    return response

