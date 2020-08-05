from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote
from api.communications.serializers import ContestDebatesSerializer, ContestCodeNotesSerializer, VelogsSerializer
from api.users.models import CustomProfile



class CustomProfileSerializer(serializers.ModelSerializer):
    isProfileMine=serializers.SerializerMethodField()
    myContests=serializers.SerializerMethodField()
    myContestsNow= serializers.SerializerMethodField()
    myContestsFinished=serializers.SerializerMethodField()
    contestDebates=serializers.SerializerMethodField()
    contestCodeNotes=serializers.SerializerMethodField()
    velogs=serializers.SerializerMethodField()


    class Meta:
        model = CustomProfile
        fields=['SmallImage','nickname','contestRankDictionary']
    def get_isProfileMine(self,obj):
        return self.context.user == obj.user

    def get_myContests(self,obj):
        list = []
        for  contest in obj.myContests():
            list.append(contest.id)
        return list


    def get_myContestsNow(self,obj):
        list = []
        for contest in obj.myContestsNow():
            list.append({"id":contest.id,"title":contest.title})
        return list

    def get_myContestsFinished(self,obj):
        list = []
        for contest in obj.myContestsFinished():
            list.append({"id":contest.id,"title":contest.title})
        return list

    def get_contestDebates(self,obj):

        contestDebates= ContestDebate.objects.filter(writer=obj.user)
        serializer=ContestDebatesSerializer(contestDebates, many=True)

        return serializer.data

    def get_contestCodeNotes(self,obj):
        contestCodeNotes = ContestCodeNote.objects.filter(writer=obj.user)
        serializer = ContestCodeNotesSerializer(contestCodeNotes, many=True)

        return serializer.data

    def get_velogs(self, obj):

        velogs = ContestCodeNote.objects.filter(writer=obj.user)
        serializer = VelogsSerializer(velogs, many=True)

        return serializer.data


class CustomProfileSerializerForWrite(serializers.ModelSerializer):

    class Meta:
        model = CustomProfile
        fields = ['Image', 'nickname', 'contestRankDictionary', 'user', 'phoneNumber', 'email']
        read_only_fields = ['user', 'email', 'phoneNumber', 'contestRankDictionary',]

