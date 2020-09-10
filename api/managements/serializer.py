from rest_framework import serializers

from api.managements.models import Notice, QuestionToManager, CommentToQuestion, FeedbackToManager
from config.serializer import IsOwnerMixin


class WriterNicknameImageSerializer(serializers.ModelSerializer):
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')


class NoticesSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = Notice
        exclude = ['updatedAt', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class NoticeSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'isPinned']


class NoticeSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ['hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class QuestionsToManagerSerializer(WriterNicknameImageSerializer, IsOwnerMixin):
    class Meta:
        model = QuestionToManager
        exclude = ['updatedAt']
        read_only_fields = ['hitNums', 'createdAt', 'isPrivate']


class QuestionToManagerSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = QuestionToManager
        fields = ['title', 'content', 'isPrivate']


class QuestionToManagerSerializer(WriterNicknameImageSerializer, IsOwnerMixin):
    class Meta:
        model = QuestionToManager
        exclude = ['writer']
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class CommentToQuestionSerializer(WriterNicknameImageSerializer, IsOwnerMixin):
    class Meta:
        model = CommentToQuestion
        fields = '__all__'
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class CommentToQuestionSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = CommentToQuestion
        fields = ['content']


class CommentsToQuestionSerializer(WriterNicknameImageSerializer, IsOwnerMixin):
    class Meta:
        model = CommentToQuestion
        fields = '__all__'
        read_only_fields = ['hitNums', 'createdAt', 'updatedAt', 'writer']


class FeedbacksToManagerSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = FeedbackToManager
        exclude = ['content']


class FeedbackToManagerSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = FeedbackToManager
        fields = ['title', 'content']


class FeedbackToManagerSerializer(WriterNicknameImageSerializer):
    class Meta:
        model = FeedbackToManager
        fields = '__all__'
