from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, \
    VelogComment


# 댓글은 좋아요만 있고, 글은 좋아요와 스크랩 모두 있다. 그래서 둘을 분리해놓고 글과 댓글의 serializer에 상속시킨 것이다.
# 복수형은 글 목록에 띄울 것들이다.

class LikeIncludedModelSerializer(serializers.ModelSerializer):
    likeNums = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    writerNickname = serializers.SerializerMethodField()
    writerImage = serializers.SerializerMethodField()

    def get_isLiked(self, obj):
        user = self.context.get("user")
        if user:
            if True:  # user.is_authenticated:
                return user in obj.likes.all()
        return False

    def get_likeNums(self, obj):
        return obj.likes.count()

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        return None

    def get_writerImage(self, obj):
        if obj.writer.customProfile.smallImage:
            return obj.writer.customProfile.smallImage


class LikeScrapIncludedModelSerializer(LikeIncludedModelSerializer):
    isScraped = serializers.SerializerMethodField()
    scrapNums = serializers.SerializerMethodField()

    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user:
            if user.is_authenticated:  # user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False

    def get_scrapNums(self, obj):
        return obj.scrapsCount()


# 단수형과 복수형이 용도가 다름.

class ContestDebatesSerializer(LikeScrapIncludedModelSerializer):
    class Meta:
        model = ContestDebate
        exclude = ['updatedAt', 'likes', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class ContestDebateSerializer(LikeScrapIncludedModelSerializer):
    class Meta:
        model = ContestDebate
        exclude = ['likes']
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class ContestCodeNotesSerializer(LikeScrapIncludedModelSerializer):
    class Meta:
        model = ContestCodeNote
        exclude = ['updatedAt', 'likes', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class ContestCodeNoteSerializer(LikeScrapIncludedModelSerializer):
    class Meta:
        model = ContestCodeNote
        exclude = ['likes']
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class VelogsSerializer(LikeScrapIncludedModelSerializer):
    class Meta:
        model = Velog
        exclude = ['likes', 'createdAt', 'content']
        read_only_fields = ['createdAt', 'hitNums']
        extra_kwargs = {'writer': {'write_only': True}}


class VelogSerializer(LikeScrapIncludedModelSerializer):
    class Meta:
        model = Velog
        exclude = ['likes']
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}


class DebateCommentSerializer(LikeIncludedModelSerializer):
    class Meta:
        model = DebateComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestDebate': {'write_only': True}}


class CodeNoteCommentSerializer(LikeIncludedModelSerializer):
    class Meta:
        model = CodeNoteComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestCodeNote': {'write_only': True}}


class VelogCommentSerializer(LikeIncludedModelSerializer):
    class Meta:
        model = VelogComment
        exclude = ['likes', ]
        read_only_fields = ['createdAt', 'hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestCodeNote': {'write_only': True}}
