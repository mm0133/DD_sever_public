from django.contrib.auth.models import User
from django.db import models

# 삭제할 때 view에서, 대댓이 있는 걸 확인해서 있으면 '삭제된 댓글입니다'로 content를 바꾼다.
# 대댓 없으면 그냥 지운다.


class Notice(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    isPinned = models.BooleanField(default=False)  # 상단 고정 공지냐 아니냐

    def __str__(self):
        return self.title

    # 글 쓸 권한 확인을 위해 내장함수를 쓰려고 했으나,
    # is_staff 내장함수가 있어서 view에서 한 줄 더 적어주면 된다.


class QuestionToManager(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()
    hitNums = models.IntegerField(default=0)

    title = models.CharField(max_length=255)

    isPrivate = models.BooleanField()
    # 질문글이 공개냐 비공개냐. 일부러 default 안 줘서 validate error 나게 유도.
    #유저가 수정 불가하게 함
    def __str__(self):
        return self.title


class CommentToQuestion(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    content = models.TextField()
    hitNums = models.IntegerField(default=0)

    questionToManager = models.ForeignKey(QuestionToManager, on_delete=models.CASCADE)

    # 대댓글(재귀)
    commentToQuestion = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    # 이 글에 댓글을 쓸 수 있는가 없는가
    def isPrivileged(self, request):
        if request.user.is_staff or request.user == self.writer:
            return True
        else:
            return False


# 그냥 받고 끝인 피드백
class FeedbackToManager(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
