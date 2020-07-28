from django.db import models
from api.communications.models import ContestCodeNote, ContestDebate, Velog
from api.contests.models import Contest, ContestUserAnswer
from api.contests.utils import user_profile_image_path
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default.png", upload_to=user_profile_image_path, null=True, blank=True
    )
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=11, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)

    # json으로 어떤 대회에서(id값이 key가 된다) 어떤 rank(1~5)를 들고 있는지 기록해둔다.
    contestRankDictionary = models.TextField(default="{}")

    contestScrpas = models.ManyToManyField(Contest, blank=True)
    debateScraps = models.ManyToManyField(ContestDebate, blank=True)
    codeNoteScraps = models.ManyToManyField(ContestCodeNote, blank=True)
    velogScraps = models.ManyToManyField(Velog, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def myContests(self):
        return ContestUserAnswer.objects.filter(writer=self.user).order_by("-createdAt")

    def myContestsNow(self):
        myContests = ContestUserAnswer.objects.filter(writer=self.user).order_by(
            "-createdAt"
        )
        returnList = []
        for contest in myContests:
            if not contest.isFinished:
                returnList.append(contest)
        return returnList

    def myContestsFinished(self):
        myContests = ContestUserAnswer.objects.filter(writer=self.user).order_by(
            "-createdAt"
        )
        returnList = []
        for contest in myContests:
            if contest.isFinished:
                returnList.append(contest)
        return returnList
