from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from api.contests.validators import validate_file_size
from config.FilePath import contestContestAnswerPath, contestFileFilePath, contestParticipantAnswerFilePath, \
    contestProfileThumbPath, contestBackThumbPath
from django_mysql.models import ListTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class Contest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # step 만 가능
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # 채점을 위한 data 를 contestAnswer 에 저장함.
    contestAnswer = models.FileField(
        null=True, blank=True, max_length=255, upload_to=contestContestAnswerPath
    )
    deadline = models.DateTimeField()
    timeline = models.TextField()  # 여러 날짜들을 text 로 저장했다가 json 으로 변환해서 프론트로 넘김
    prize = models.IntegerField()  # 만 단위로 받을 것임.

    isForTraining = models.BooleanField(default=False)  # 연습용이냐 실전용이냐.

    winnerInterview = models.TextField(
        null=True, blank=True
    )  # 우승자 인터뷰 & 코드 리뷰 영상. 유튜브 URL 만 db 에서 들고 있게 한다.

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
                                       max_length=255, upload_to=contestProfileThumbPath,
                                       processors=[Thumbnail(256, 256)],  # 처리할 작업 목룍
                                       format='JPEG',  # 최종 저장 포맷
                                       options={'quality': 90},
                                       default="user_1/profile",
                                       )
    backThumb = ProcessedImageField(null=True, blank=True,
                                    max_length=255, upload_to=contestBackThumbPath,
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
    file = models.FileField(max_length=255, upload_to=contestFileFilePath, null=True, blank=True)  # data file 을 위함


class ContestParticipantAnswer(models.Model):
    contest = models.ForeignKey(
        Contest, null=True, on_delete=models.SET_NULL, related_name="userAnswer"
    )
    team = models.ForeignKey(
        'users.Team', null=True, blank=True, on_delete=models.SET_NULL, related_name="teamAnswer"
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    isTeam = models.BooleanField(default=False)
    teamMembers = ListTextField(null=True, blank=True, base_field=models.CharField(max_length=255), )
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    file = models.FileField(max_length=255, upload_to=contestParticipantAnswerFilePath, null=True, blank=True,
                            validators=[validate_file_size])

    accuracy = models.FloatField(default=0)

    # 종료 시점에 업데이트해서 1등 - 1, 2등 - 2, 3등 - 3, 상위30% - 4 참여완료 - 5
    rank = models.IntegerField(default=0)

    likes = models.ManyToManyField(User, related_name='contestAnswerLikes', blank=True)

    def get_name(self):
        if self.isTeam and self.team:
            return self.team.name
        elif (not self.isTeam) and self.user:
            return self.user.customProfile.nickname
        else:
            return "삭제된 계정"

    def calculateAccuracy(self):
        # self.file 로 계산하는 로직넣기
        return 50

    @property
    def likesCount(self):
        return self.likes.count()

    @property
    def rating(self):
        if self.contest.evaluationMethod == "ACCURACY":
            return self.accuracy
        else:
            return self.likesCount()

    def __str__(self):
        # 3항 연산자
        teamOrUser = 'team' if self.isTeam else 'user'
        return f'answer by {teamOrUser} {self.name} to {self.contest.title}'
