from django.db import models
from django.db.models import Q

from api.communications.models import ContestCodeNote, ContestDebate, Velog
from api.contests.models import Contest, ContestParticipantAnswer
from django.contrib.auth.models import User
from api.educations.models import LecturePackage
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from config.FilePath import customProfileImagePath, customProfileSmallImage, teamSmallImagePath, teamImagePath


class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customProfile")
    image = ProcessedImageField(null=True, blank=True,
                                max_length=255, upload_to=customProfileImagePath,
                                processors=[Thumbnail(256, 256)],
                                format='JPEG',
                                options={'quality': 85},
                                default="user_1/profile",
                                )
    smallImage = ProcessedImageField(null=True, blank=True,
                                     max_length=255, upload_to=customProfileSmallImage,
                                     processors=[Thumbnail(64, 64)],
                                     format='JPEG',
                                     options={'quality': 60},
                                     default="user_1/profile",
                                     )

    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=11, unique=True)
    nickname = models.CharField(max_length=255, unique=True)

    # json으로 어떤 대회에서(id값이 key가 된다) 어떤 rank(1~5)를 들고 있는지 기록해둔다.
    contestRankDictionary = models.TextField(default="{}")

    contestScraps = models.ManyToManyField(Contest, related_name="scrapProfiles", blank=True)
    debateScraps = models.ManyToManyField(ContestDebate, related_name="scrapProfiles", blank=True)
    codeNoteScraps = models.ManyToManyField(ContestCodeNote, related_name="scrapProfiles", blank=True)
    velogScraps = models.ManyToManyField(Velog, related_name="scrapProfiles", blank=True)
    createdAT = models.DateTimeField(auto_now_add=True)
    updatedAT = models.DateTimeField(auto_now=True)

    isRealNameAuthenticated = models.BooleanField(default=False)
    isConsentingEmail = models.BooleanField(default=False)  # 홍보성 메일 수신 동의 # 중요 메일은 무조건 수신해야 함.
    isConsentingSMS = models.BooleanField(default=False)
    lecturePackages = models.ManyToManyField(LecturePackage, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def myContests(self):
        myContestAnswers = ContestParticipantAnswer.objects \
            .filter(Q(user=self.user) | Q(teamMembers__contains=self.user.customProfile.nickname)) \
            .order_by("-createdAt")
        return myContestAnswers

    def myContestsNow(self):
        myContestAnswers = self.myContests()
        returnList = []
        for contestAnswer in myContestAnswers:
            if not contestAnswer.contest.isFinished:
                returnList.append(contestAnswer.contest)
        return returnList

    def myContestsFinished(self):
        myContestAnswers = self.myContests()
        returnList = []
        for contestAnswer in myContestAnswers:
            if contestAnswer.contest.isFinished:
                returnList.append(contestAnswer.contest)
        return returnList


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(null=True, blank=True,
                                max_length=255, upload_to=teamImagePath,
                                processors=[Thumbnail(256, 256)],  # 처리할 작업 목룍
                                format='JPEG',  # 최종 저장 포맷
                                options={'quality': 85},
                                default="user_1/profile",
                                )
    smallImage = ProcessedImageField(null=True, blank=True,
                                     max_length=255, upload_to=teamSmallImagePath,
                                     processors=[Thumbnail(64, 64)],  # 처리할 작업 목룍
                                     format='JPEG',  # 최종 저장 포맷
                                     options={'quality': 85},
                                     default="user_1/profile",
                                     )

    representative = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                                       related_name='representingTeam')  # delete 조심히 할것
    members = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return f"Team {self.name} "

class TeamInvite(models.Model):
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE, related_name="teamInvite")
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teamInviteReceived')
    invitingMessage = models.TextField(blank=True, null=True)
    isAccepted = models.BooleanField(default=False)
    isFinished = models.BooleanField(default=False)

    def __str__(self):
        return f"teamInvite from team {self.team.name}' to {self.invitee.customProfile.nickname}"

