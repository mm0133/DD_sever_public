from rest_framework import serializers
from api.educations.models import EduVideoLecture, LecturePackage


class WriterNicknameImageSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    def get_writerNickname(self, obj):
        if obj.writer.customProfile.nickname:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer.customProfile.smallImage:
            return obj.writer.customProfile.smallImage
        else:
            return None


class LecturePackageSerializer(WriterNicknameImageSerializer):
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
