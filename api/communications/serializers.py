from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, VelogComment



class LikeIncludedModelSerializer(serializers.ModelSerializer):
    likeNums = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    writerNickname = serializers.SerializerMethodField()

    def get_isLiked(self, obj):

        user = self.context.get("user")
        if user:
            if True:  # user.is_authenticated:
                user in obj.likes.all()
        return False

    def get_likeNums(self, obj):
        return obj.likes.count()

    def get_writerNickname(self, obj):
        if obj.writer:
            return obj.writer.customProfile.nickname
        return None


class LikeScrapIncludedModelSerializer(LikeIncludedModelSerializer):

    isScraped=serializers.SerializerMethodField()
    scrapNums = serializers.SerializerMethodField()

    def get_isScraped(self, obj):
        user = self.context.get("user")
        if user:
            if user.is_authenticated:#user.is_authenticated: 로그인시
                return obj.isScraped(user)
        return False

    def get_scrapNums(self,obj):
        return obj.scrapsCount()



class ContestDebatesSerializer(LikeScrapIncludedModelSerializer):


    class Meta:
        model = ContestDebate
        exclude = ['updatedAt','likes', 'content']
        read_only_fields= ['createdAT','hitNums']
        extra_kwargs={'writer':{'write_only':True}}



class ContestDebateSerializer(LikeScrapIncludedModelSerializer):


    class Meta:
        model = ContestDebate
        exclude = ['likes']
        read_only_fields= ['createdAT','hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}



class ContestCodeNotesSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = ContestCodeNote
        exclude = ['updatedAt', 'likes', 'content']
        read_only_fields= ['createdAT','hitNums']
        extra_kwargs={'writer':{'write_only':True}}


class ContestCodeNoteSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = ContestCodeNote
        exclude = ['likes']
        read_only_fields= ['createdAT','hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}



class VelogsSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = Velog
        exclude = ['likes', 'createdAt', 'content']
        read_only_fields= ['createdAT','hitNums']
        extra_kwargs={'writer':{'write_only':True}}


class VelogSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model=Velog
        exclude = ['likes']
        read_only_fields= ['createdAT','hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}}



class DebateCommentSerializer(LikeIncludedModelSerializer):

    class Meta:
        model=DebateComment
        exclude = ['likes', ]
        read_only_fields= ['createdAT','hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestDebate':{'write_only': True}}

class CodeNoteCommentSerializer(LikeIncludedModelSerializer):

    class Meta:
        model=CodeNoteComment
        exclude = ['likes', ]
        read_only_fields= ['createdAT','hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestCodeNote':{'write_only': True}}



class VelogCommentSerializer(LikeIncludedModelSerializer):

    class Meta:
        model=VelogComment
        exclude = ['likes', ]
        read_only_fields= ['createdAT','hitNums', 'updatedAt']
        extra_kwargs = {'writer': {'write_only': True}, 'contestCodeNote':{'write_only': True}}


# class ContestDebatesSerializer(serializers.ModelSerializer):
#
#     likeNums=serializers.SerializerMethodField()
#     isLiked=serializers.SerializerMethodField()
#     isScraped=serializers.SerializerMethodField()
#
#     class Meta:
#         model = ContestDebate
#         exclude = ['updatedAt','likes', 'content']
#
#
#     def get_isLiked(self, obj):
#         user = self.context.get("user")
#         if user:
#             if True: #user.is_authenticated:
#                 user in obj.likes.all()
#         return False
#
#
#     def get_likeNums(self, obj):
#         return obj.likes.count()
#
#     def get_isScraped(self, obj):
#         user = self.context.get("user")
#         if user:
#             if user.is_authenticated:#user.is_authenticated: 로그인시
#                 return obj in user.customProfile.debateScraps.all()
#         return False

# class ContestDebateSerializer(serializers.ModelSerializer):
#
#     likeNums=serializers.SerializerMethodField()
#     isLiked=serializers.SerializerMethodField()
#     isScraped=serializers.SerializerMethodField()
#
#     class Meta:
#         model = ContestDebate
#         exclude = ['likes']
#
#     def get_isLiked(self, obj):
#         request = self.context.get("request")
#         if request:
#             user = request.user
#             if True: #user.is_authenticated:
#                 user in obj.likes.all()
#         return False
#
#
#     def get_likeNums(self, obj):
#         return obj.likes.count()
#
#     def get_isScraped(self, obj):
#         request = self.context.get("request")
#         if request:
#             user = request.user
#             if user.is_authenticated:#user.is_authenticated: 로그인시
#                 return obj in user.profile.codeNoteScraps.all()
#         return False
#
#
# class ContestCodeNotesSerializer(serializers.ModelSerializer):
#     likeNums = serializers.SerializerMethodField()
#     isLiked = serializers.SerializerMethodField()
#     isScraped = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ContestDebate
#         exclude = ['updatedAt', 'likes', 'content']
#
#     def get_isLiked(self, obj):
#         request = self.context.get("request")
#         if request:
#             user = request.user
#             if True:  # user.is_authenticated:
#                 user in obj.likes.all()
#         return False
#
#     def get_likeNums(self, obj):
#         return obj.likes.count()
#
#     def get_isScraped(self, obj):
#         request = self.context.get("request")
#         if request:
#             user = request.user
#             if user.is_authenticated:  # user.is_authenticated: 로그인시
#                 return obj in user.customProfile.codeNoteScraps.all()
#         return False
#
# class ContestCodeNoteSerializer(serializers.ModelSerializer):
#     likeNums = serializers.SerializerMethodField()
#     isLiked = serializers.SerializerMethodField()
#     isScraped = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ContestDebate
#         exclude = ['updatedAt', 'likes', 'content']
#
#     def get_isLiked(self, obj):
#         user = self.context.get("user")
#         if user:
#             if True:  # user.is_authenticated:
#                 user in obj.likes.all()
#         return False
#
#     def get_likeNums(self, obj):
#         return obj.likes.count()
#
#     def get_isScraped(self, obj):
#         request = self.context.get("request")
#         if request:
#             user = request.user
#             if user.is_authenticated:  # user.is_authenticated: 로그인시
#                 return obj in user.customProfile.codeNoteScraps.all()
#         return False





