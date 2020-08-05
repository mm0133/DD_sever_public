from rest_framework import serializers

from api.managements.models import Notice, QuestionToManager, CommentToQuestion, FeedbackToManager


class NoticesSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content']
        read_only_fields = ['createdAT', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

class NoticesSerializerExcludeIsPinned(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content']
        read_only_fields = ['createdAT', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None


class NoticeSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields='__all__'
        read_only_fields=['hitNums']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None


class QuestionsToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        exclude=['writer','updatedAt']
        read_only_fields = ['hitNums', 'createdAT', 'isPrivate']

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None


class QuestionToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = QuestionToManager
        exclude = ['writer']
        read_only_fields = ['hitNums','createdAT','updatedAT']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None


class CommentToQuestionSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()

    class Meta:
        model = CommentToQuestion
        fields='__all__'
        read_only_fields=['hitNums', 'createdAT', 'updatedAT']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None


class  FeedbacksToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    class Meta:
        model = FeedbackToManager
        exclude = ['content']


    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

class  FeedbackToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    class Meta:
        model = FeedbackToManager
        fields='__all__'


    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        return None