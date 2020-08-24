from encodings.utf_8 import encode
from encodings.utf_8_sig import decode

from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote, Velog
from api.communications.serializer import ContestDebatesSerializer, ContestCodeNotesSerializer, VelogsSerializer
from api.contests.models import Contest
from api.users.models import CustomProfile, Team, TeamInvite
from api.users.utils import validate_phoneNumber


class ContestSerializerForScrap(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ["id", "profileThumb", "title"]


class DebateSerializerForScrap(serializers.ModelSerializer):
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')

    class Meta:
        model = ContestDebate
        fields = ["id", "title", "writerNickname", "writerImage"]


class CodenoteSerializerForScrap(serializers.ModelSerializer):
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')

    class Meta:
        model = ContestCodeNote
        fields = ["id", "title", "writerNickname", "writerImage"]


class VelogSerializerForScrap(serializers.ModelSerializer):
    writerNickname = serializers.CharField(source='writer.customProfile.nickname')
    writerImage = serializers.ImageField(source='writer.customProfile.smallImage')

    class Meta:
        model = Velog
        fields = ["id", "title", "writerNickname", "writerImage"]


class MyCustomProfileSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()
    myContestsNow = serializers.SerializerMethodField()
    myContestsFinished = serializers.SerializerMethodField()
    contestDebates = serializers.SerializerMethodField()
    contestCodeNotes = serializers.SerializerMethodField()
    velogs = serializers.SerializerMethodField()

    contestScraps = serializers.SerializerMethodField()
    debateScraps = serializers.SerializerMethodField()
    codenoteScraps = serializers.SerializerMethodField()
    velogScraps = serializers.SerializerMethodField()

    class Meta:
        model = CustomProfile
        fields = ['image', 'user', 'nickname', 'contestRankDictionary',
                  'teams', 'myContestsNow', 'myContestsFinished',
                  'contestDebates', 'contestCodeNotes', 'velogs',
                  'contestScraps', 'debateScraps', 'codenoteScraps', 'velogScraps']

    def get_teams(self, obj):
        teams = obj.user.teams
        serializer = TeamsSerializer(teams, many=True)
        return serializer.data

    def get_myContestsNow(self, obj):
        list = []
        for contest in obj.myContestsNow():
            list.append({"id": contest.id, "title": contest.title})
        return list

    def get_myContestsFinished(self, obj):
        list = []
        for contest in obj.myContestsFinished():
            list.append({"id": contest.id, "title": contest.title})
        return list

    def get_contestDebates(self, obj):

        contestDebates = ContestDebate.objects.filter(writer=obj.user)
        serializer = ContestDebatesSerializer(contestDebates, many=True, context={"user": obj.user})

        return serializer.data

    def get_contestCodeNotes(self, obj):
        contestCodeNotes = ContestCodeNote.objects.filter(writer=obj.user)
        serializer = ContestCodeNotesSerializer(contestCodeNotes, many=True, context={"user": obj.user})

        return serializer.data

    def get_velogs(self, obj):

        velogs = Velog.objects.filter(writer=obj.user)
        serializer = VelogsSerializer(velogs, many=True, context={"user": obj.user})

        return serializer.data

    def get_contestScraps(self, obj):
        contestScraps = obj.contestScraps.all()
        return ContestSerializerForScrap(contestScraps, many=True, context={"user": obj.user}).data

    def get_debateScraps(self, obj):
        debateScraps = obj.contestScraps.all()
        return DebateSerializerForScrap(debateScraps, many=True, context={"user": obj.user}).data

    def get_codenoteScraps(self, obj):
        codenoteScraps = obj.codeNoteScraps.all()
        return DebateSerializerForScrap(codenoteScraps, many=True, context={"user": obj.user}).data

    def get_velogScraps(self, obj):
        velogScraps = obj.velogScraps.all()
        return VelogSerializerForScrap(velogScraps, many=True, context={"user": obj.user}).data


class CustomProfileSerializer(serializers.ModelSerializer):
    velogs = serializers.SerializerMethodField()

    class Meta:
        model = CustomProfile
        fields = ['image', 'nickname', 'contestRankDictionary', 'velogs']

    def get_velogs(self, obj):
        velogs = Velog.objects.filter(writer=obj.user)
        serializer = VelogsSerializer(velogs, many=True)

        return serializer.data


class CustomProfileSerializerForChange(serializers.ModelSerializer):
    class Meta:
        model = CustomProfile
        fields = ['nickname', 'phoneNumber', 'email', 'image']

    def validate_nickname(self, value):
        if get_object_or_None(CustomProfile, nickname=value):
            raise serializers.ValidationError("This nickname already exists.")
        else:
            return value

    def validate_phoneNumber(self, value):
        if get_object_or_None(CustomProfile, phoneNumber=value):
            raise serializers.ValidationError("This phoneNumber already exists.")
        elif not validate_phoneNumber(value):
            raise serializers.ValidationError("phoneNumber must be 11 digit and start with 01")
        else:
            return value

    def validate_email(self, value):
        if get_object_or_None(CustomProfile, email=value):
            raise serializers.ValidationError("This email already exists.")
        else:
            return value


class MemberSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='customProfile.nickname')
    smallImage = serializers.ImageField(source='customProfile.smallImage')

    class Meta:
        model = User
        fields = ['nickname', 'smallImage']


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'representative', 'smallImage']


class TeamsSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'image']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    isRepresentative = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'representative', 'members', 'smallImage', 'createdAt', 'isRepresentative']

    def get_members(self, obj):
        members = obj.members.all()
        return MemberSerializer(members, many=True).data

    def get_isRepresentative(self, obj):
        user = self.context.get("user")
        return user == obj.representative


class TeamInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvite
        fields = "__all__"


class TeamInviteSerializerForAccept(serializers.ModelSerializer):
    class Meta:
        model = TeamInvite
        fields = ["isAccepted"]
        extra_kwargs = {'isAccepted': {'required': True}}


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)

    def validate_newPassword(self, value):
        validate_password(value)
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
