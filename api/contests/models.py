from typing import TYPE_CHECKING

from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from imagekit.processors import Thumbnail
from imagekit.models import ProcessedImageField

from api.contests.utils import comp_answer_upload_to, user_answer_upload_to
from api.contests.validators import validate_file_size




class Contest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # step만 가능
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # 채점을 위한 data를 contestAnswer에 저장함.
    contestAnswer = models.FileField(
        null=True, blank=True, upload_to=comp_answer_upload_to
    )
    deadline = models.DateTimeField()
    timeline = models.TextField()  # 여러 날짜들을 text로 저장했다가 json으로 변환해서 프론트로 넘김
    prize = models.IntegerField()  # 만 단위로 받을 것임.

    isForTraining = models.BooleanField(default=False)  # 연습용이냐 실전용이냐.

    winnerInterview = models.TextField(
        null=True, blank=True
    )  # 우승자 인터뷰 & 코드 리뷰 영상. 유튜브 URL만 db에서 들고 있게 한다.

    # 등급(초중고)
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"
    difficultyChoice = ((EASY, "Easy"), (NORMAL, "Normal"), (HARD, "Hard"))
    difficulty = models.CharField(
        max_length=6, choices=difficultyChoice, default="Normal"
    )

    # 평가방법(정확도 vs 인기도(추천순))
    ACCURACY = "ACCURACY"
    POPULARITY = "POPULARITY"
    evaluationChoice = ((ACCURACY, "Accuracy"), (POPULARITY, "Popularity"))
    evaluationMethod = models.CharField(
        max_length=10, choices=evaluationChoice, default="Accuracy"
    )

    # 학습 모델 종류. 계속 추가될 것이므로 따로 선택지를 고정해놓지는 않는다.
    learningModel = models.CharField(max_length=255)

    evaluationExplanation = models.TextField()  # 평가기준 설명
    contestExplanation = models.TextField()  # 대회 설명
    prizeExplanation = models.TextField()  # 상금 설명
    dataExplanation = models.TextField()  # data 설명
    profileThumb = ProcessedImageField(null=True, blank=True,
                                       upload_to='',
                                       processors=[Thumbnail(256, 256)],  # 처리할 작업 목룍
                                       format='JPEG',  # 최종 저장 포맷
                                       options={'quality': 90},
                                       default="user_1/profile",
                                       )
    backThumb = ProcessedImageField(null=True, blank=True,
                                    upload_to='',
                                    processors=[Thumbnail(256, 256)],  # 처리할 작업 목룍
                                    format='JPEG',  # 최종 저장 포맷
                                    options={'quality': 90},
                                    default="user_1/profile",
                                    )
    contestOverview = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def isFinished(self):
        now = timezone.now()
        if self.deadline < now:
            return True
        else:
            return False

    def scrapsCount(self):
        return self.scrapProfiles.count()

    def isScraped(self, user):
        return user.customProfile in self.scrapProfiles.all()


class ContestFile(models.Model):
    contest = models.ForeignKey(Contest, null=True, on_delete=models.SET_NULL)
    file = models.FileField(null=True, blank=True)  # data file을 위함


class ContestUserAnswer(models.Model):
    contest = models.ForeignKey(
        Contest, null=True, on_delete=models.SET_NULL, related_name="userAnswer"
    )
    team = models.ForeignKey(
        'users.Team', null=True, on_delete=models.SET_NULL, related_name="teamAnswer"
    )
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    file = models.FileField(upload_to='', null=True, blank=True, validators=[validate_file_size])

    accuracy = models.FloatField(default=0)

    # 종료 시점에 업데이트해서 1등 - 1, 2등 - 2, 3등 - 3, 상위30% - 4 참여완료 - 5
    rank = models.IntegerField(default=0)

    def calculateAccuracy(self):
        # self.file로 계산하는 로직넣기
        return 50
