from rest_framework import serializers

from api.contests.models import Contest, ContestFile, ContestUserAnswer


class ContestsSerializer(serializers.ModelSerializer):
    isScraped=serializers.SerializerMethodField()
    scrapNums = serializers.SerializerMethodField()
    isFinished=serializers.SerializerMethodField()

    class Meta:
        model=Contest
        fields= ['id', 'title', 'createdAt', 'updatedAt','deadline', 'profileThumb'
                 'timeline','prize', 'isForTraining', 'difficulty', 'evaluationMethod',
                'learningModel' ]


    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user:
            if user.is_authenticated:#user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False

    def get_scrapNums(self,obj):
        return obj.scrapsCount()

    def get_isFinished(self, obj):
        return obj.isFinished()




class ContestSerializer(serializers.ModelSerializer):
    isScraped=serializers.SerializerMethodField()
    scrapNums = serializers.SerializerMethodField()
    isFinished=serializers.SerializerMethodField()

    class Meta:
        model:Contest
        fields=['id', 'writer', 'title', 'createdAt', 'updatedAt', 'contestAnswer','deadline',
                'timeline', 'prize', 'isForTraining', 'winnerInterview',  'difficulty', 'evaluationMethod',
                'learningModel', 'evaluationExplanation', 'contestExplanation', 'prizeExplanation', 'dataExplanation'
                'profileThumb', 'backThumb', 'contestOverview'
                ]
        extra_kwargs = {'writer': {'write_only': True},
                        'contestAnswer':{'write_only':True}}



    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user:
            if user.is_authenticated:#user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False

    def get_scrapNums(self,obj):
        return obj.scrapsCount()

    def get_isFinished(self, obj):
        return obj.isFinished()

class ContestScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields=['id', 'contest', 'file']

class ContestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestFile
        fields=['id','contest', 'file']
        extra_kwargs = {'contest': {'write_only': True}}


class ContestUserAnswerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = ContestUserAnswer
        fields= ['id','contest', 'writer', 'createdAt', 'updatedAt', 'file', 'accuracy', 'rank']
        read_only_fields= ['createdAT', 'updatedAt','rank']
        extra_kwargs = {'contest': {'write_only': True},
                        'writer':{'write_only':True},
                        'file':{'write_only':True}}

        def get_writerNickname(self, obj):
            if obj.writer:
                return obj.writer.customProfile.nickname
            return None
        #accuracy
