from rest_framework import serializers

from api.managements.models import Notice, QuestionToManager, CommentToQuestion, FeedbackToManager


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


class NoticesSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class NoticesSerializerExcludeIsPinned(WriterNicknameImageSerializer):
    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content', 'isPinned']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class NoticeSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ['hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class QuestionsToManagerSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = QuestionToManager
        exclude = ['updatedAt']
        read_only_fields = ['hitNums', 'createdAt', 'isPrivate']


class QuestionToManagerSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = QuestionToManager
        exclude = ['writer']
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class CommentToQuestionSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = CommentToQuestion
        fields = '__all__'
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class CommentsToQuestionSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = CommentToQuestion
        fields = '__all__'
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt', 'writer']


class FeedbacksToManagerSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = FeedbackToManager
        exclude = ['content']


class FeedbackToManagerSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = FeedbackToManager
        fields = '__all__'
