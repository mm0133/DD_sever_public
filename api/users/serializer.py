from rest_framework import serializers

from api.communications.models import ContestDebate, ContestCodeNote
from api.users.models import CustomProfile


class ProfileSerializer(serializers.ModelSerializer):
    myContests=serializers.SerializerMethodField()
    myContestsNow= serializers.SerializerMethodField()
    myContestsFinished=serializers.SerializerMethodField()
    contestDebates=serializers.SerializerMethodField()
    contestCodeNotes=serializers.SerializerMethodField()
    velog=serializers.SerializerMethodField()


    class Meta:
        model = CustomProfile
        fields=['image','nickname','contestRankDictionary']

    def get_myContests(self,obj):
        list = []
        for  contest in obj.myContests():
            list.append(contest.id)
        return list



    def get_myContestsNow(self,obj):
        list = []
        for contest in obj.myContestsNow():
            list.append(contest.id)
        return list

    def get_myContestsFinished(self,obj):
        list = []
        for contest in obj.myContestsFinished():
            list.append(contest.id)
        return list

    def get_contestDebates(self,obj):
        list = []
        for debate in ContestDebate.objects.filter(writer=obj.user):
            list.append({"id":debate.id, "title":debate.title})
            return list

    def get_contestCodeNote(self,obj):
        list = []
        for codeNote in ContestCodeNote.objects.filter(writer=obj.user):
            list.append(codeNote.id)
            return list

    # def get_velog(self, obj):
    #     list = []
    #     for


