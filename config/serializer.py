from rest_framework import serializers


class IsOwnerMixin(serializers.Serializer):
    isOwner = serializers.SerializerMethodField()

    def get_isOwner(self, obj):
        user = self.context.get("user")
        return user and user.is_authenticated and obj.writer == user
