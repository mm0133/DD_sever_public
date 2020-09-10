from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from api.managements.models import Notice, QuestionToManager, FeedbackToManager, CommentToQuestion
from api.managements.serializer import NoticesSerializer, NoticeSerializer, FeedbacksToManagerSerializer, \
    FeedbackToManagerSerializer, QuestionsToManagerSerializer, QuestionToManagerSerializer, \
    CommentToQuestionSerializer, CommentsToQuestionSerializer, NoticeSerializerForPost, \
    QuestionToManagerSerializerForPost, CommentToQuestionSerializerForPost, FeedbackToManagerSerializerForPost
from config.customPermissions import IsGetRequestOrAdminUser, IsGetRequestOrAuthenticated
from config.customExceptions import get_object_or_404_custom, DDCustomException

from config.utils import HitCountResponse, DDCustomListAPiView


class NoticeListView(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAdminUser]
    queryset = Notice.objects.all().order_by('-id')
    serializer_class = NoticesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    def list(self, request, *args, **kwargs):
        isPinned = request.GET.get('isPinned')
        if isPinned == 'true':
            rawQueryset = self.get_queryset().filter(isPinned=True)
        elif isPinned == 'false':
            rawQueryset = self.get_queryset().filter(isPinned=False)
        else:
            rawQueryset = self.get_queryset()

        queryset = self.filter_queryset(rawQueryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NoticesSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = NoticesSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class NoticeCreateView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def post(self, request):
        serializer = NoticeSerializerForPost(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            notice = serializer.save(writer=request.user)
            returnSerializer = NoticesSerializer(notice, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notice = get_object_or_404_custom(Notice, pk=pk)
        notice.delete()
        return Response(status=status.HTTP_200_OK)


class QuestionToManagerListView(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAdminUser]
    queryset = QuestionToManager.objects.all().order_by('-id')
    serializer_class = QuestionsToManagerSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    def list(self, request, *args, **kwargs):
        isPrivate = request.GET.get('isPrivate')
        isMine = request.GET.get('isMine')

        if request.user.is_staff:
            if isPrivate == 'true':
                rawQueryset = self.get_queryset().filter(isPrivate=True)
            elif isPrivate == 'false':
                rawQueryset = self.get_queryset().filter(isPrivate=False)
            else:
                rawQueryset = self.get_queryset()
        else:
            rawQueryset = self.get_queryset().filter(isPrivate=False)

        if isMine == 'true':
            rawQueryset = rawQueryset.filter(writer=request.user)

        queryset = self.filter_queryset(rawQueryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = QuestionsToManagerSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = QuestionsToManagerSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class QuestionToManagerCreateView(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def post(self, request):
        serializer = QuestionToManagerSerializerForPost(data=request.data)
        if serializer.is_valid():
            question = serializer.save(writer=request.user)
            returnSerializer = QuestionToManagerSerializer(question, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이친구는 get_QuestionToManager 에서 접근 권한을 제한했음
class QuestionToManagerViewWithPk(APIView):

    def get_questionToManager(self, request, pk):
        questionToManager = get_object_or_404_custom(QuestionToManager, pk=pk)
        if (not questionToManager.isPrivate) \
                or (request.user == questionToManager.writer) \
                or request.user.is_staff:
            return questionToManager
        else:
            raise DDCustomException('당신은 이 questionToManager에 접근할 권한이 없습니다.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

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
        questionToManager = get_object_or_404_custom(QuestionToManager, pk=pk)
        commentToQuestion = CommentToQuestion.objects.filter(questionToManager=questionToManager)

        if (not questionToManager.isPrivate) or \
                request.user == questionToManager.writer or \
                request.user.is_staff:
            serializer = CommentsToQuestionSerializer(commentToQuestion, many=True, context={"user": request.user})
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk):
        questionToManager = get_object_or_404_custom(QuestionToManager, pk=pk)
        if questionToManager.writer != request.user and \
                not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        commentToQuestion_id = request.data.get('commentToQuestion_id')
        if commentToQuestion_id:
            parent_commentToQuestion = get_object_or_404_custom(CommentToQuestion, pk=commentToQuestion_id)
        else:
            parent_commentToQuestion = None
        serializer = CommentToQuestionSerializerForPost(data=request.data)
        if serializer.is_valid():
            commentToQuestion = serializer.save(writer=request.user, questionToManager=questionToManager,
                                                commentToQuestion=parent_commentToQuestion)
            returnSerializer = CommentToQuestionSerializer(commentToQuestion, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정삭제, get 요청은 잘안쓸거같긴한데 나중에 혹시 ajax 에서 쓸수있으니 구현해놈
class CommentToQuestionViewWithCommentPK(APIView):

    def get_commentToQuestion(self, request, pk):
        commentToQuestion = get_object_or_404_custom(CommentToQuestion, pk=pk)
        if (not commentToQuestion.questionToManager.isPrivate) or \
                commentToQuestion.isPrivileged(request):
            return commentToQuestion
        else:
            raise DDCustomException('당신은 이 commentToQuestion에 접근할 권한이 없습니다.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(request, pk)
        serializer = CommentToQuestionSerializer(commentToQuestion, context={"user": request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(request, pk)
        if not commentToQuestion.isPrivileged(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # 바꿀 게 하나밖에 없어서 serializer 안 쓰고 그냥 객체에 직접 접근함.
        commentToQuestion.content = request.data.get("content")
        commentToQuestion.save()

        return Response(CommentToQuestionSerializer(commentToQuestion).data)

    def delete(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(request, pk)
        commentToQuestion.delete()
        return Response(status=status.HTTP_200_OK)


class FeedbackToManagerListView(DDCustomListAPiView):
    permission_classes = [IsAdminUser]
    queryset = FeedbackToManager.objects.all().order_by('-id')
    serializer_class = FeedbacksToManagerSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('id',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FeedbacksToManagerSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = FeedbacksToManagerSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class FeedbackToManagerCreateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedbackToManagerSerializerForPost(data=request.data)
        if serializer.is_valid():
            feedbackToManager = serializer.save(writer=request.user)
            returnSerializer = FeedbackToManagerSerializer(feedbackToManager, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
