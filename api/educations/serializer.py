from rest_framework import serializers
from api.educations.models import EduVideoLecture

class EduVideoLecturesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EduVideoLecture
        exclude = ['videoURL']


class EduVideoLectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = EduVideoLecture
        fields = "__all__"




