from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, \
    VelogComment
from config.serializer import IsOwnerMixin


# 댓글은 좋아요만 있고, 글은 좋아요와 스크랩 모두 있다. 그래서 둘을 분리해놓고 글과 댓글의 serializer 에 상속시킨 것이다.
# 복수형은 글 목록에 띄울 것들이다.

class LikeIncludedModelSerializer(serializers.ModelSerializer):
    isLiked = serializers.SerializerMethodField()
    likeNums = serializers.IntegerField(source='likes.count')
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')

    def get_isLiked(self, obj):
        user = self.context.get("user")
        if user:
            if user.is_authenticated:
                return user in obj.likes.all()
        return False


class LikeScrapIncludedModelSerializer(LikeIncludedModelSerializer):
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.IntegerField(source='scrapsCount')

    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user.is_authenticated:
            return obj.isScraped(user)
        return False


class LikeScrapContestTitleIncludedModelSerializer(LikeScrapIncludedModelSerializer):
    contestTitle = serializers.CharField(source='contest.title')


# 단수형과 복수형이 용도가 다름.

class ContestDebateSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = ContestDebate
        fields = ['title', 'content', 'id']
        read_only_fields = ['id']


class ContestCodenoteSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = ContestCodeNote
        fields = ['title', 'content', 'id']
        read_only_fields = ['id']


class ContestDebatesSerializer(LikeScrapContestTitleIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = ContestDebate
        exclude = ['updatedAt', 'likes', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class ContestDebateSerializer(LikeScrapContestTitleIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = ContestDebate
        exclude = ['likes']
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class ContestCodeNotesSerializer(LikeScrapContestTitleIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = ContestCodeNote
        exclude = ['updatedAt', 'likes', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class ContestCodeNoteSerializer(LikeScrapContestTitleIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = ContestCodeNote
        exclude = ['likes']
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class VelogsSerializer(LikeScrapIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = Velog
        exclude = ['likes', 'createdAt', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class VelogSerializer(LikeScrapIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = Velog
        exclude = ['likes']
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class DebateCommentSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = DebateComment
        fields = ['content', 'id']
        read_only_fields = ['id']


class CodeNoteCommentSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = CodeNoteComment
        fields = ['content', 'id']
        read_only_fields = ['id']


class VelogCommentSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = VelogComment
        fields = ['content', 'id']
        read_only_fields = ['id']


class DebateCommentSerializer(LikeIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = DebateComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestDebate': {'write_only': True}}


class CodeNoteCommentSerializer(LikeIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = CodeNoteComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestCodeNote': {'write_only': True}}


class VelogCommentSerializer(LikeIncludedModelSerializer, IsOwnerMixin):
    class Meta:
        model = VelogComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestCodeNote': {'write_only': True}}
