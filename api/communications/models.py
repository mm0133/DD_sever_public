from django.db import models
from django.contrib.auth.models import User
from api.contests.models import Contest


class IsTemporaryAttributeManager(models.Manager):
    def get_queryset(self):
        return super(IsTemporaryAttributeManager, self).get_queryset()\
            .filter(isTemporary=False)


class ContestDebate(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)

    # like는 여기 두고 스크랩은 유저의 profile에 둘 것이다.
    likes = models.ManyToManyField(User, related_name="contestDebateLikes", blank=True)

    isTemporary = models.BooleanField(default=False)

    objects = models.Manager()
    dd_objects = IsTemporaryAttributeManager()

    def __str__(self):
        return self.title

    def scrapsCount(self):
        # profile에 many-to-many를 걸어놨기 때문에 역참조한 것이다.
        return self.scrapProfiles.count()

    def isScraped(self, user):
        return user.customProfile in self.scrapProfiles.all()


class ContestCodeNote(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    contest = models.ForeignKey(Contest, null=True, on_delete=models.SET_NULL)

    # like는 여기 두고 스크랩은 유저의 profile에 둘 것이다.
    likes = models.ManyToManyField(
        User, related_name="contestCodeNoteLikes", blank=True
    )

    isTemporary = models.BooleanField(default=False)

    objects = models.Manager()
    dd_objects = IsTemporaryAttributeManager()
    def __str__(self):
        return self.title

    def scrapsCount(self):
        return self.scrapProfiles.count()

    def isScraped(self, user):
        return user.customProfile in self.scrapProfiles.all()


class Velog(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    # like는 여기 두고 스크랩은 유저의 profile에 둘 것이다.
    likes = models.ManyToManyField(
        User, related_name="velogLikes", blank=True
    )

    isTemporary = models.BooleanField(default=False)

    objects = models.Manager()
    dd_objects = IsTemporaryAttributeManager()

    def __str__(self):
        return self.title

    def scrapsCount(self):
        return self.scrapProfiles.count()

    def isScraped(self, user):
        return user.customProfile in self.scrapProfiles.all()


class DebateComment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    contestDebate = models.ForeignKey(ContestDebate, null=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="debateCommentLikes", blank=True
    )

    # 대댓글(재귀)
    debateComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )


# 결투장 code에 comment
class CodeNoteComment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    contestCodeNote = models.ForeignKey(ContestCodeNote, null=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="codeNoteCommentLikes", blank=True
    )

    # 대댓글(재귀)
    codeNoteComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )


class VelogComment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()

    velog = models.ForeignKey(Velog, null=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, related_name="velogCommentLikes", blank=True
    )

    # 대댓글(재귀)
    velogComment = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
