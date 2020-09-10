from rest_framework import serializers

from api.communications.serializer import LikeIncludedModelSerializer
from api.educations.models import EduVideoLecture, LecturePackage, LecturePackageComment, EduVideoLectureComment
from config.serializer import IsOwnerMixin


class WriterNicknameImageSerializer(serializers.ModelSerializer):
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')


class LecturePackageSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = LecturePackage
        fields = "__all__"


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


class LecturePackageCommentSerializerForPostPUT(serializers.ModelSerializer):
    class Meta:
        model = LecturePackageComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class LecturePackageCommentSerializer(LikeIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = LecturePackageComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class EduVideoLectureCommentSerializerForPostPut(serializers.ModelSerializer):
    class Meta:
        model = EduVideoLectureComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class EduVideoLectureCommentSerializer(LikeIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = EduVideoLectureComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}
