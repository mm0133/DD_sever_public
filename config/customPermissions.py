from rest_framework import permissions


class IsGetRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "GET"


class IsPostRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class IsPutRequest(permissions.BasePermission):
    def has_permission(selfs, request, view):
        return request.method == "PUT"


class IsDeleteRequest(permissions.BasePermission):
    def has_permission(selfs, request, view):
        return request.method == "DELETE"


# IsAuthenticatedOrReadOnly
class IsGetRequestOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated) or request.method == "GET")


class IsGetRequestOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_staff) or request.method == "GET")


class IsGetRequestOrWriterOrAdminUser(permissions.BasePermission):
    # 작성자만 접근, 작성자가 아니면 Read만 가능
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method == "GET":
                return True
            elif obj.writer == request.user:
                return True
            elif request.user.is_staff:
                return True
            return False
        else:
            return False


class IsWriterOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and ((request.user.is_authenticated and request.user == obj.writer) or request.user.is_staff):
            return True
        return False


class IsRepresentativeOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and (
                (request.user.is_authenticated and request.user == obj.representative) or request.user.is_staff):
            return True
        return False
