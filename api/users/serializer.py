from encodings.utf_8 import encode
from encodings.utf_8_sig import decode

from django.contrib.auth.models import User
from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote, Velog
from api.communications.serializers import ContestDebatesSerializer, ContestCodeNotesSerializer, VelogsSerializer
from api.users.models import CustomProfile, Team


class MyCustomProfileSerializer(serializers.ModelSerializer):
    myContestsNow = serializers.SerializerMethodField()
    myContestsFinished = serializers.SerializerMethodField()
    contestDebates = serializers.SerializerMethodField()
    contestCodeNotes = serializers.SerializerMethodField()
    velogs = serializers.SerializerMethodField()

    contestScraps = serializers.SerializerMethodField()
    debateScraps = serializers.SerializerMethodField()
    codeNoteScraps = serializers.SerializerMethodField()
    velogScraps = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    class Meta:
        model = CustomProfile
        fields = ['image', 'user', 'nickname', 'contestRankDictionary', 'myContestsNow', 'myContestsFinished',
                  'contestDebates', 'contestCodeNotes', 'velogs', 'contestScraps', 'debateScraps', 'codeNoteScraps',
                  'velogScraps', 'teams']

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
        serializer = ContestDebatesSerializer(contestDebates, many=True)

        return serializer.data

    def get_contestCodeNotes(self, obj):
        contestCodeNotes = ContestCodeNote.objects.filter(writer=obj.user)
        serializer = ContestCodeNotesSerializer(contestCodeNotes, many=True)

        return serializer.data

    def get_velogs(self, obj):

        velogs = Velog.objects.filter(writer=obj.user)
        serializer = VelogsSerializer(velogs, many=True)

        return serializer.data

    def get_contestScraps(self, obj):
        contestScrapList = obj.contestScraps.all()
        if contestScrapList:
            list = []
            for contest in contestScrapList:
                list.append({"id": contest.id, "profileThumb": contest.profileThumb, "title": contest.title})
            return list
        else:
            return None

    def get_debateScraps(self, obj):
        debateScrapList = obj.debateScraps.all()
        if debateScrapList:
            list = []
            for debate in debateScrapList:
                list.append({"id": debate.id, "writerNickname": debate.writer.customProfile.nickname,
                             "writerImage": debate.writer.customProfile.smallImage, "title": debate.title})
            return list
        return None

    def get_codeNoteScraps(self, obj):
        codeNoteScrapList = obj.codeNoteScraps.all()
        if codeNoteScrapList:
            list = []
            for codeNote in codeNoteScrapList:
                list.append({"id": codeNote.id, "writerNickname": codeNote.writer.customProfile.nickname,
                             "writerImage": codeNote.writer.customProfile.smallImage, "title": codeNote.title})
            return list
        return None

    def get_velogScraps(self, obj):
        velogScrapList = obj.velogScraps.all()
        if velogScrapList:
            list = []
            for velog in velogScrapList:
                list.append({"id": velog.id, "writerNickname": velog.writer.customProfile.nickname,
                             "writerImage": velog.writer.customProfile.smallImage, "title": velog.title})
            return list
        return None

    def get_teams(self, obj):
        teams = obj.user.teams
        serializer = TeamsSerializer(teams, many=True)
        return serializer.data


class CustomProfileSerializer(serializers.ModelSerializer):
    velogs = serializers.SerializerMethodField()

    class Meta:
        model = CustomProfile
        fields = ['image', 'nickname', 'contestRankDictionary', 'velogs']

    def get_velogs(self, obj):
        velogs = Velog.objects.filter(writer=obj.user)
        serializer = VelogsSerializer(velogs, many=True)

        return serializer.data


class CustomProfileSerializerForOwner(serializers.ModelSerializer):
    class Meta:
        model = CustomProfile
        fields = ['image', 'nickname', 'user', 'phoneNumber', 'email']
        read_only_fields = ['user', 'email', 'phoneNumber']  # 현재 read only 핗요없긴함 혹시몰라남김


class CustomProfileSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model = CustomProfile
        fields = ['nickname', 'contestRankDictionary', 'user', 'phoneNumber', 'email', 'image']


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
