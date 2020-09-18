from django.contrib.auth.models import User
from django.db import models
from imagekit.generatorlibrary import Thumbnail
from imagekit.models import ProcessedImageField

from config.utils import ddAnonymousUser
from config.FilePath import lecturePackageThumbnailPath

class LecturePackage(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    hitNums = models.IntegerField(default=0)
    thumbnail = ProcessedImageField(null=True, blank=True,
                                    max_length=255, upload_to=lecturePackageThumbnailPath,
                                    processors=[Thumbnail(256, 256)],  # 처리할 작업 목룍
                                    format='JPEG',  # 최종 저장 포맷
                                    options={'quality': 90},
                                    default="user_1/profile",
                                    )

    title = models.CharField(max_length=255)  # 제목은 무조건 달아야 함!

    isCharged = models.BooleanField(default=False)  # 유료냐 무료냐

    packageExplanation = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class EduVideoLecture(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    hitNums = models.IntegerField(default=0)

    videoURL = models.TextField(null=True, blank=True)
    videoExplanation = models.TextField(null=True, blank=True)

    title = models.CharField(max_length=255)  # 제목은 무조건 달아야 함!

    lecturePackage = models.ForeignKey(LecturePackage, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class LecturePackageComment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='myLecturePackageComments')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    lecturePackage = models.ForeignKey(LecturePackage, null=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="LecturePackageCommentLikes", blank=True
    )

    # 대댓글(재귀)
    lecturePackageComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f'comment (id: {self.id}) by {self.writer.customProfile.nickname} \
        on lecturePackage {self.lecturePackage.title}'


class EduVideoLectureComment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    eduVideoLecture = models.ForeignKey(EduVideoLecture, null=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="EduVideoLectureCommentLikes", blank=True
    )

    # 대댓글(재귀)
    eduVideoLectureComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f'comment (id: {self.id}) by {self.writer.customProfile.nickname} \
        on eduVideoLecture {self.eduVideoLecture.title} \
        of lecturePackage {self.eduVideoLecture.lecturePackage.title}'
