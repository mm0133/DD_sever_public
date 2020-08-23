from rest_framework import serializers
from api.educations.models import EduVideoLecture, LecturePackage
from config.serializers import IsOwnerMixin



class WriterNicknameImageSerializer(serializers.ModelSerializer):

    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')




class LecturePackageSerializerForPost(serializers.ModelSerializer):
    IsOwner=serializers.SerializerMethodField()

    class Meta:
        model = LecturePackage
        fields = "__all__"

    def get_IsOwnser(self, obj):
        user=self.context.get("user")
        return user and obj.writer == user and user.is_authenticate


class LecturePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturePackage
        fields = "__all__"


class EduVideoLecturesSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = EduVideoLecture
        exclude = ['videoURL']


class EduVideoLectureSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = EduVideoLecture
        fields = "__all__"
