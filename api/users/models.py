from django.db import models
from api.communications.models import ContestCodeNote, ContestDebate, Velog
from api.contests.models import Contest, ContestUserAnswer
from api.contests.utils import user_profile_image_path, team_profile_image_path
from django.contrib.auth.models import User
from api.educations.models import LecturePackage
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customProfile")
    image = ProcessedImageField(null=True, blank=True,
                                upload_to=user_profile_image_path,
                                processors=[Thumbnail(256, 256)],
                                format='JPEG',
                                options={'quality': 60},
                                default="user_5/profile",
                                )
    smallImage = ProcessedImageField(null=True, blank=True,
                                     upload_to=user_profile_image_path,
                                     processors=[Thumbnail(64, 64)],
                                     format='JPEG',
                                     options={'quality': 60},
                                     default="user_5/profile",
                                     )

    email = models.EmailField()
    phoneNumber = models.CharField(max_length=11)
    nickname = models.CharField(max_length=255)

    # json으로 어떤 대회에서(id값이 key가 된다) 어떤 rank(1~5)를 들고 있는지 기록해둔다.
    contestRankDictionary = models.TextField(default="{}")

    contestScraps = models.ManyToManyField(Contest, related_name="scrapProfiles", blank=True)
    debateScraps = models.ManyToManyField(ContestDebate, related_name="scrapProfiles", blank=True)
    codeNoteScraps = models.ManyToManyField(ContestCodeNote, related_name="scrapProfiles", blank=True)
    velogScraps = models.ManyToManyField(Velog, related_name="scrapProfiles", blank=True)
    createdAT = models.DateTimeField(auto_now_add=True)
    updatedAT = models.DateTimeField(auto_now=True)

    isRealNameAuthenticated = models.BooleanField(default=False)
    isConsentingEmail = models.BooleanField(default=False)
    isConsentingSMS = models.BooleanField(default=False)
    lecturePackages = models.ManyToManyField(LecturePackage, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def myContests(self):
        return ContestUserAnswer.objects.filter(writer=self.user).order_by("-createdAt")

    def myContestsNow(self):
        myContestAnswers = ContestUserAnswer.objects.filter(writer=self.user).order_by(
            "-createdAt"
        )
        returnList = []
        for contestAnswer in myContestAnswers:
            if not contestAnswer.contest.isFinished:
                returnList.append(contestAnswer.contest)
        return returnList

    def myContestsFinished(self):
        myContestAnswers = ContestUserAnswer.objects.filter(writer=self.user).order_by(
            "-createdAt"
        )
        returnList = []
        for contestAnswer in myContestAnswers:
            if contestAnswer.contest.isFinished:
                returnList.append(contestAnswer.contest)
        return returnList


class Team(models.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    smallImage = ProcessedImageField(null=True, blank=True,
                                     upload_to=team_profile_image_path,
                                     processors=[Thumbnail(64, 64)],  # 처리할 작업 목룍
                                     format='JPEG',  # 최종 저장 포맷
                                     options={'quality': 60},
                                     default="user_6/profile",
                                     )

    representative = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                                       related_name='representingTeam')  # delete 조심히 할것
    members = models.ManyToManyField(User, related_name='teams')

    def __str__(self):
        return f"Team {self.name} "
