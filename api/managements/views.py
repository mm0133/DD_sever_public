from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from api.managements.models import Notice, QuestionToManager, FeedbackToManager, CommentToQuestion
from api.managements.serializer import NoticesSerializer, NoticeSerializer, FeedbacksToManagerSerializer, \
    FeedbackToManagerSerializer, QuestionsToManagerSerializer, QuestionToManagerSerializer, \
    CommentToQuestionSerializer, NoticesSerializerExcludeIsPinned, CommentsToQuestionSerializer
from config.customPermissions import IsGetRequestOrAdminUser, IsGetRequestOrAuthenticated
from config.customExceptions import get_object_or_404_custom


from config.utils import HitCountResponse


class NoticeView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request):
        notice = Notice.objects.all()
        serializer = NoticesSerializer(notice, many=True, context={"user": request.user})
        return Response(serializer.data)

    def post(self, request):
        serializer = NoticeSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def pinnedNotice(request):
    notice = Notice.objects.filter(isPinned=True)
    serializer = NoticesSerializerExcludeIsPinned(notice, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def notpinnedNotie(request):
    notice = Notice.objects.filter(isPinned=False)
    serializer = NoticesSerializerExcludeIsPinned(notice, many=True)
    return Response(serializer.data)


class NoticeViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        notice = get_object_or_404_custom(Notice, pk=pk)
        serializer = NoticeSerializer(notice, context={"user": request.user})
        return HitCountResponse(request, notice, Response(serializer.data))

    def put(self, request, pk):
        notice = get_object_or_404_custom(Notice, pk=pk)

        serializer = NoticeSerializer(notice, data=request.data, partial=True, context={"user": request.user})
        if serializer.is_valid():  # validate 로직 추가
            notice = serializer.save()
            return Response(NoticeSerializer(notice).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notice = get_object_or_404_custom(Notice, pk=pk)
        notice.delete()
        return Response(status=status.HTTP_200_OK)


class QuestionToManagerView(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            questionToManager = QuestionToManager.objects.all()
        else:
            questionToManager = QuestionToManager.objects.filter(isPrivate=False)

        serializer = QuestionsToManagerSerializer(questionToManager, many=True, context={"user": request.user})
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionToManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_privateQuestionToManager(request):
    if request.user.is_staff:
        questionToManager = QuestionToManager.objects.filter(isPrivate=True)
    elif request.user.is_authenticated:
        questionToManager = QuestionToManager.objects.filter(isPrivate=True, writer=request.user)
    else:
        questionToManager = None

    serializer = QuestionsToManagerSerializer(questionToManager, many=True, context={"user": request.user})
    return Response(serializer.data)


@api_view(['GET'])
def get_publicQuestionToManager(request):
    questionToManager = QuestionToManager.objects.filter(isPrivate=False)
    serializer = QuestionsToManagerSerializer(questionToManager, many=True, context={"user": request.user})
    return Response(serializer.data)


@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def get_MyQuestionToManager(request):
    questionToManager = QuestionToManager.objects.filter(writer=request.user)
    serializer = QuestionsToManagerSerializer(questionToManager, many=True, context={"user": request.user})
    return Response(serializer.data)


# 이친구는 get_QuestionToManager 에서 접근 권한을 제한했음
class QuestionToManagerViewWithPk(APIView):

    def get_questionToManager(self, request, pk):
        questionToManager = get_object_or_404_custom(QuestionToManager, pk=pk)
        if (not questionToManager.isPrivate) \
                or (request.user == questionToManager.writer) \
                or request.user.is_staff:
            return questionToManager
        else:
            raise PermissionDenied

    def get(self, request, pk):
        questionToManager = self.get_questionToManager(request, pk)
        serializer = QuestionToManagerSerializer(questionToManager, context={"user": request.user})
        return HitCountResponse(request, questionToManager, Response(serializer.data))

    def put(self, request, pk):
        questionToManager = self.get_questionToManager(request, pk)

        serializer = QuestionToManagerSerializer(questionToManager, data=request.data, partial=True,
                                                 context={"user": request.user})
        if serializer.is_valid():
            questionToManager = serializer.save()
            return Response(QuestionToManagerSerializer(questionToManager).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        questionToManager = self.get_questionToManager(request, pk)
        questionToManager.delete()
        return Response(status=status.HTTP_200_OK)


class CommentToQuestionViewWithQuestionPK(APIView):
    def get(self, request, pk):
        questionToManager = QuestionToManager.objects.get(pk=pk)
        commentToQuestion = CommentToQuestion.objects.filter(questionToManager_id=pk)

        if (not questionToManager.isPrivate) or \
                request.user == questionToManager.writer or \
                request.user.is_staff:
            serializer = CommentsToQuestionSerializer(commentToQuestion, many=True, context={"user": request.user})
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk):
        if QuestionToManager.objects.get(pk=pk).writer != request.user and \
                not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if 'commentToQuestion' in request.data:
            commentToQuestion_id = request.data['commentToQuestion']
            # 다른 questionToManager 에 달려 있는 commentToQuestion 대댓을 달지 못하게 하는 코드
            parent_debateComment = get_object_or_404_custom(CommentToQuestion, pk=commentToQuestion_id)
            if parent_debateComment.questionToManager.id is not pk:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            commentToQuestion_id = None

        commentToQuestion = CommentToQuestion.objects.create(
            writer=request.user,
            content=request.data["content"],
            questionToManager_id=pk,
            commentToQuestion_id=commentToQuestion_id
        )
        serializer = CommentToQuestionSerializer(commentToQuestion, context={"user": request.user})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈
class CommentToQuestionViewWithCommentPK(APIView):

    def get_commentToQuestion(self, request, pk):
        commentToQuestion = get_object_or_404_custom(CommentToQuestion, pk=pk)
        if (not commentToQuestion.questionToManager.isPrivate) or \
                commentToQuestion.isPrivileged(request):
            return commentToQuestion
        else:
            raise PermissionDenied

    def get(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(request, pk)
        serializer = CommentToQuestionSerializer(commentToQuestion, context={"user": request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(request, pk)
        if not commentToQuestion.isPrivileged(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # 바꿀 게 하나밖에 없어서 serializer 안 쓰고 그냥 객체에 직접 접근함.
        commentToQuestion.content = request.data["content"]
        commentToQuestion.save()

        return Response(CommentToQuestionSerializer(commentToQuestion).data)

    def delete(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(request, pk)
        commentToQuestion.delete()
        return Response(status=status.HTTP_200_OK)


class FeedbackToManagerView(APIView):
    def get(self, request):
        if not request.user.is_staff:  # 관리자가 아니라면
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        feedbackToManager = FeedbackToManager.objects.all()
        serializer = FeedbacksToManagerSerializer(feedbackToManager, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedbackToManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 수정기능 불필요해서 put 구현 안 함.
class FeedbackToManagerViewWithPk(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        feedbackToManager = get_object_or_404_custom(FeedbackToManager, pk=pk)
        serializer = FeedbackToManagerSerializer(feedbackToManager)
        return Response(serializer.data)

    def delete(self, request, pk):
        feedbackToManager = get_object_or_404_custom(FeedbackToManager, pk=pk)
        feedbackToManager.delete()
        return Response(status=status.HTTP_200_OK)
