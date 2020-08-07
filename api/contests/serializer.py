from django.contrib.auth.models import User
from rest_framework import serializers

from api.contests.models import Contest, ContestFile, ContestUserAnswer


class ContestsSerializer(serializers.ModelSerializer):
    # serializer에서는 Contest.objects.all() 이런 식으로 객체를 직접 가져오지 못한다.
    # 따라서 별도로 object의 attribute를 불러와주는 방법이 필요한데,
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.SerializerMethodField()
    isFinished = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ['id', 'title', 'createdAt', 'updatedAt', 'deadline', 'profileThumb',
                  'timeline', 'prize', 'isForTraining', 'difficulty', 'evaluationMethod',
                  'learningModel',
                  'isScraped', 'scrapNums', 'isFinished']
        read_only_fields = ['isScraped', 'scrapNums', 'isFinished']

    def get_isScraped(self, obj):
        # context는 이 serializer를 호출할 때 넘겨준다. contest.views를 보면 확인 가능하다.
        user = self.context.get("user")
        if user:
            if user.is_authenticated:  # user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False

    def get_scrapNums(self, obj):
        return obj.scrapsCount()

    def get_isFinished(self, obj):
        return obj.isFinished()


class ContestSerializer(serializers.ModelSerializer):
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.SerializerMethodField()
    isFinished = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ['id', 'writer', 'title', 'createdAt', 'updatedAt', 'contestAnswer', 'deadline',
                  'timeline', 'prize', 'isForTraining', 'winnerInterview', 'difficulty', 'evaluationMethod',
                  'learningModel', 'evaluationExplanation', 'contestExplanation', 'prizeExplanation', 'dataExplanation',
                  'profileThumb', 'backThumb', 'contestOverview',
                  'isScraped', 'scrapNums', 'isFinished',
                  ]
        extra_kwargs = {'writer': {'write_only': True},
                        'contestAnswer': {'write_only': True}}

    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user:
            if user.is_authenticated:  # user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False

    def get_scrapNums(self, obj):
        return obj.scrapsCount()

    def get_isFinished(self, obj):
        return obj.isFinished()


class ContestScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'contest', 'file']


class ContestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestFile
        fields = ['id', 'contest', 'file']
        extra_kwargs = {'contest': {'write_only': True}}


class ContestUserAnswerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = ContestUserAnswer
        fields = ['id', 'contest', 'writer', 'createdAt', 'updatedAt', 'file', 'accuracy', 'rank', 'writerNickname']
        read_only_fields = ['createdAT', 'updatedAt', 'rank', 'writerNickname']
        extra_kwargs = {'contest': {'write_only': True},
                        'writer': {'write_only': True},
                        'file': {'write_only': True}}

        def get_writerNickname(self, obj):
            if obj.writer:
                return obj.writer.customProfile.nickname
            return None
        # accuracy
