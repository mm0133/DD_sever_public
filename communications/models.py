from django.db import models
from django.contrib.auth.models import User
from communications.models import Contest


# 삭제할 때 view에서, 대댓이 있는 걸 확인해서 있으면 '삭제된 댓글입니다'로 content를 바꾼다.
# 대댓 없으면 그냥 지운다.


# ContestDebate와 ContestCodePost는 모델 상 정확히 똑같지만, 다르게 쓴다.
class ContestDebate(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL)

    # like는 여기 두고 스크랩은 유저의 profile에 둘 것이다.
    like = models.ManyToManyField(
        User, related_name="ContestDebateLikes", null=True, blank=True
    )

    def __str__(self):
        return self.title

    def scrapsCount(self):
        return User.objects.filter(debateScraps=self).count()


class ContestCodeNote(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL)

    # like는 여기 두고 스크랩은 유저의 profile에 둘 것이다.
    likes = models.ManyToManyField(
        User, related_name="compost_likes", null=True, blank=True
    )

    def __str__(self):
        return self.title

    def scrapsCount(self):
        return User.objects.filter(codeNoteScraps=self).count()


class Velog(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    # like는 여기 두고 스크랩은 유저의 profile에 둘 것이다.
    likes = models.ManyToManyField(
        User, related_name="compost_likes", null=True, blank=True
    )

    def __str__(self):
        return self.title

    def scrapsCount(self):
        return User.objects.filter(velogScraps=self).count()


class DebateComment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    contestDebate = models.ForeignKey(ContestDebate, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="debateCommentLikes", null=True, blank=True
    )

    # 대댓글(재귀)
    debateComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )


# 결투장 code에 comment
class CodeNoteComment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    contestCodeNote = models.ForeignKey(ContestCodeNote, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="codeNoteCommentLikes", null=True, blank=True
    )

    # 대댓글(재귀)
    codeNoteComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )


class VelogComment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    velog = models.ForeignKey(Velog, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="velogLikes", null=True, blank=True
    )

    # 대댓글(재귀)
    VelogComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
