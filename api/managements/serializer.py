from rest_framework import serializers

from api.managements.models import Notice, QuestionToManager, CommentToQuestion, FeedbackToManager


class NoticesSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class NoticesSerializerExcludeIsPinned(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content', 'isPinned']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class NoticeSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ['hitNums']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class QuestionsToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        exclude = ['writer', 'updatedAt']
        read_only_fields = ['hitNums', 'createdAt', 'isPrivate']

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class QuestionToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = QuestionToManager
        exclude = ['writer']
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class CommentToQuestionSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = CommentToQuestion
        fields = '__all__'
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class FeedbacksToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackToManager
        exclude = ['content']

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        else:
            return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage


class FeedbackToManagerSerializer(serializers.ModelSerializer):
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackToManager
        fields = '__all__'

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        return None

    def get_writerImage(self, obj):
        if obj.writer:
            return obj.writer.customProfile.SmallImage
