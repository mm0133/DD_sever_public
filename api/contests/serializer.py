from annoying.functions import get_object_or_None
from django.contrib.auth.models import User

from api.contests.models import Contest, ContestFile, ContestParticipantAnswer
from rest_framework import serializers
from os.path import basename

from config.utils import ddAnonymousUser


class ContestsSerializer(serializers.ModelSerializer):
    # serializer 에서는 Contest.objects.all() 이런 식으로 객체를 직접 가져오지 못한다.
    # 따라서 별도로 object 의 attribute 를 불러와주는 방법이 필요한데,
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.IntegerField(source='scrapsCount')
    participantNumber = serializers.IntegerField(source='participantAnswer.count')

    class Meta:
        model = Contest
        fields = ['id', 'title', 'subtitle', 'createdAt', 'updatedAt', 'deadline', 'profileThumb',
                  'timeline', 'prize', 'isForTraining', 'difficulty', 'evaluationMethod', 'learningModel',
                  'isScraped', 'scrapNums', 'isFinished', 'participantNumber']
        read_only_fields = ['isScraped', 'scrapNums', 'isFinished', 'participantNumber']

    def get_isScraped(self, obj):
        # context 는 이 serializer 를 호출할 때 넘겨준다. contest.views 를 보면 확인 가능하다.
        user = self.context.get("user")
        if user:
            if user.is_authenticated:  # user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False


class ContestSerializer(serializers.ModelSerializer):
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.IntegerField(source='scrapsCount')
    participantNumber = serializers.IntegerField(source='participantAnswer.count')

    class Meta:
        model = Contest
        fields = ['id', 'writer', 'title', 'subtitle', 'createdAt', 'updatedAt', 'contestAnswer', 'deadline',
                  'timeline', 'prize', 'isForTraining', 'winnerInterview', 'difficulty', 'evaluationMethod',
                  'learningModel', 'evaluationExplanation', 'contestExplanation', 'prizeExplanation', 'dataExplanation',
                  'profileThumb', 'backThumb',
                  'isScraped', 'scrapNums', 'isFinished', 'participantNumber']
        read_only_fields = ['isScraped', 'scrapNums', 'isFinished', 'participantNumber']
        extra_kwargs = {'writer': {'write_only': True},
                        'contestAnswer': {'write_only': True}}

    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user.is_authenticated:
            return obj.isScraped(user)
        return False


class ContestSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['title', 'subtitle', 'contestAnswer', 'deadline',
                  'timeline', 'prize', 'isForTraining', 'winnerInterview', 'difficulty', 'evaluationMethod',
                  'learningModel', 'evaluationExplanation', 'contestExplanation', 'prizeExplanation', 'dataExplanation',
                  'profileThumb', 'backThumb']


class ContestScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'contest', 'file']


class ContestFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)
    fileName = serializers.SerializerMethodField()
    fileSize = serializers.SerializerMethodField()

    class Meta:
        model = ContestFile
        fields = ['id', 'contest', 'file', 'fileName', 'fileSize', ]
        extra_kwargs = {'contest': {'write_only': True}}

    def get_fileName(self, obj):
        return basename(obj.file.name)

    def get_fileSize(self, obj):
        filesize = obj.file.size
        if filesize > 1048576:
            size = "%.1fMB" % (filesize / 1048576)
        elif filesize > 1024:
            size = "%dKB" % (filesize / 1024)
        else:
            size = "1KB 미만"
        return size


class ContestParticipantAnswersSerializer(serializers.ModelSerializer):
    teamMembers = serializers.ListField(source='get_teamMembers')
    isOwner = serializers.SerializerMethodField()

    class Meta:
        model = ContestParticipantAnswer
        fields = ['id', 'isTeam', 'name', 'createdAt', 'updatedAt', 'accuracy', 'rank', 'teamMembers', 'isOwner']

    def get_isOwner(self, obj):
        user = self.context.get('user')
        if obj.isTeam:
            return user and user.is_authenticated and user == obj.team.representative
        else:
            return user and user.is_authenticated and user == obj.user




class ContestParticipantAnswerSerializer(serializers.ModelSerializer):
    teamMembers = serializers.ListField()
    isOwner = serializers.SerializerMethodField()

    class Meta:
        model = ContestParticipantAnswer
        fields = ['id', 'isTeam', 'name', 'contest', 'createdAt', 'updatedAt', 'file', 'accuracy', 'rank',
                  'teamMembers', 'isOwner']
        read_only_fields = ['createdAT', 'updatedAt', 'rank', 'name', 'isTeam', 'teamMembers', 'IsOwner']
        extra_kwargs = {'contest': {'write_only': True}, }

    def get_isOwner(self, obj):
        user = self.context.get('user')
        if obj.isTeam:
            return user and user.is_authenticated and user == obj.team.representative
        else:
            return user and user.is_authenticated and user == obj.user
