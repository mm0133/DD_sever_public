from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, VelogComment

#으아 상속해서 쓰고싶은데  user에서 역참조할때 scrap들 이름이 달라서 어려움 그리고
#이걸 역참조해서 모델에 같은이름으로 함수만들까 했는데 그것도 쉽지않은게 profile에 있다는게 문제임 오류가 생기는듯?

class LikeIncludedModelSerializer(serializers.ModelSerializer):
    likeNums = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()

    def get_isLiked(self, obj):

        user = self.context.get("user")
        if user:
            if True:  # user.is_authenticated:
                user in obj.likes.all()
        return False

    def get_likeNums(self, obj):
        return obj.likes.count()


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


class ContestDebateSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = ContestDebate
        exclude = ['likes']


class ContestCodeNotesSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = ContestCodeNote
        exclude = ['updatedAt', 'likes', 'content']


class ContestCodeNoteSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = ContestCodeNote
        exclude = ['likes']



class VelogsSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model = Velog
        exclude = ['likes', 'createdAt', 'content']


class VelogSerializer(LikeScrapIncludedModelSerializer):

    class Meta:
        model=Velog
        exclude = ['likes']



class DebateCommentSerializer(LikeIncludedModelSerializer):

    class Meta:
        model=DebateComment

class CodeNoteCommentSerializer(LikeIncludedModelSerializer):

    class Meta:
        model=CodeNoteComment

class VelogCommentsSerializer(LikeIncludedModelSerializer):

    class Meta:
        model=VelogComment



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





