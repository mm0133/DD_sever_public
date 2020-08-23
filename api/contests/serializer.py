from api.contests.models import Contest, ContestFile, ContestParticipantAnswer
from rest_framework import serializers


class ContestsSerializer(serializers.ModelSerializer):
    # serializer 에서는 Contest.objects.all() 이런 식으로 객체를 직접 가져오지 못한다.
    # 따라서 별도로 object 의 attribute 를 불러와주는 방법이 필요한데,
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.IntegerField(source='scrapsCount')
    participantNumber = serializers.IntegerField(source='userAnswer.count')

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
    participantNumber = serializers.IntegerField(source='userAnswer.count')

    class Meta:
        model = Contest
        fields = ['id', 'writer', 'title', 'subtitle', 'createdAt', 'updatedAt', 'contestAnswer', 'deadline',
                  'timeline', 'prize', 'isForTraining', 'winnerInterview', 'difficulty', 'evaluationMethod',
                  'learningModel', 'evaluationExplanation', 'contestExplanation', 'prizeExplanation', 'dataExplanation',
                  'profileThumb', 'backThumb', 'contestOverview',
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
        fields = ['id', 'writer', 'title', 'subtitle', 'createdAt', 'updatedAt', 'contestAnswer', 'deadline',
                  'timeline', 'prize', 'isForTraining', 'winnerInterview', 'difficulty', 'evaluationMethod',
                  'learningModel', 'evaluationExplanation', 'contestExplanation', 'prizeExplanation', 'dataExplanation',
                  'profileThumb', 'backThumb', 'contestOverview', 'isFinished']
        extra_kwargs = {'writer': {'write_only': True},
                        'contestAnswer': {'write_only': True}}

    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user.is_authenticated:
            return obj.isScraped(user)
        return False


class ContestScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'contest', 'file']


class ContestFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = ContestFile
        fields = ['id', 'contest', 'file']
        extra_kwargs = {'contest': {'write_only': True}}


class ContestParticipantAnswersSerializer(serializers.ModelSerializer):
    teamMembers = serializers.ListField()

    class Meta:
        model = ContestParticipantAnswer
        fields = ['id', 'isTeam', 'name', 'createdAt', 'updatedAt', 'accuracy', 'rank', 'teamMembers']


class ContestParticipantAnswerSerializer(serializers.ModelSerializer):
    teamMembers = serializers.ListField()

    class Meta:
        model = ContestParticipantAnswer
        fields = ['id', 'isTeam', 'name', 'contest', 'createdAt', 'updatedAt', 'file', 'accuracy', 'rank',
                  'teamMembers']
        read_only_fields = ['createdAT', 'updatedAt', 'rank', 'name', 'isTeam', 'teamMembers']
        extra_kwargs = {'contest': {'write_only': True}, }
