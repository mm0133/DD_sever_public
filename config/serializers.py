from rest_framework import serializers


class IsOwnerMixin:
    IsOwner = serializers.SerializerMethodField()

    def get_IsOwnser(self, obj):
        user = self.context.get("user")
        return user and user.is_authenticate and obj.writer == user
