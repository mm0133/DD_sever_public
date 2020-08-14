from rest_framework import serializers
from api.educations.models import EduVideoLecture, LecturePackage


class WriterNicknameImageSerializer(serializers.ModelSerializer):
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')


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
