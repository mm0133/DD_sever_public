from django.contrib.auth.models import User
from django.db import models


class EduVideoLecture(models.Model):

    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    hitNums = models.IntegerField(default=0)

    videoURL = models.TextField(null=True, blank=True)
    videoExplanation = models.TextField(null=True, blank=True)

    title = models.CharField(max_length=255)  # 제목은 무조건 달아야 함!

    isCharged = models.BooleanField(default=False)  # 유료냐 무료냐

    def __str__(self):
        return self.title
