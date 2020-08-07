from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from api.managements.models import Notice, QuestionToManager, FeedbackToManager, CommentToQuestion
from api.managements.serializer import NoticesSerializer, NoticeSerializer, FeedbacksToManagerSerializer, \
    FeedbackToManagerSerializer, QuestionsToManagerSerializer, QuestionToManagerSerializer, \
    CommentToQuestionSerializer, NoticesSerializerExcludeIsPinned
from config.customPermissions import IsGetRequestOrAdminUser


class NoticeView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]
    def get(self, request):
        notice = Notice.objects.all()
        serializer = NoticesSerializer(notice, many=True)
        return Response(serializer.data)

    def post(self, request):
        if False:  # 관리자 인증 로직 추가
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            serializer.save(writer=request.user)  # 로그인 안하면 지금 오류남
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
    def get_notice(self, pk):
        try:
            notice = Notice.objects.get(pk=pk)
            return notice
        except notice.DoesNotExist:
            return None

    def get(self, request, pk):
        notice = self.get_notice(pk)
        if notice == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = NoticeSerializer(notice)
            return Response(serializer.data)

    def put(self, request, pk):
        notice = self.get_notice(pk)
        if notice == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # 관리자 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = NoticeSerializer(notice, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            notice = serializer.save()
            return Response(NoticeSerializer(notice).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notice = self.get_notice(pk)
        if notice == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # 관리자 인증 로직
            notice.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_privateQuestionToManager(request):
    if False:  # 관리자 로직
        questionToManager = QuestionToManager.objects.filter(isPrivate=True)
    elif True:  # 로그인 인증
        questionToManager = QuestionToManager.objects.filter(writer=request.user)

    serializer = QuestionsToManagerSerializer(questionToManager, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_publicQuestionToManager(request):
    questionToManager = QuestionToManager.objects.filter(isPrivate=False)
    serializer = QuestionsToManagerSerializer(questionToManager, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_QuestionToManager(request):
    if False:  # 로그인 인증 추가
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = QuestionToManagerSerializer(data=request.data)
    if serializer.is_valid():  # validation 로직 손보기
        serializer.save(writer=None)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이친구는 get_QuestionToManager 에서 접근 권한을 제한했음
class QuestionToManagerViewWithPk(APIView):

    def get_QuestionToManager(self, request, pk):
        try:
            questionToManager = QuestionToManager.objects.get(pk=pk)
            if (not questionToManager.isPrivate) or (request.user == questionToManager.writer and request.user.is_authenticated) \
                    or (request.user.is_staff and request.user):  # True대신에 관리자 로직 넣을것
                return questionToManager
            else:
                return None
        except questionToManager.DoesNotExist:
            return None

    def get(self, request, pk):
        questionToManager = self.get_questionToManager(request, pk)
        if questionToManager == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = QuestionToManagerSerializer(questionToManager)
            return Response(serializer.data)

    def put(self, request, pk):
        questionToManager = self.get_questionToManager(request, pk)
        if questionToManager == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user!= questionToManager.writer + 관리자가 아니면
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = QuestionToManagerSerializer(questionToManager, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            questionToManager = serializer.save()
            return Response(QuestionToManagerSerializer(questionToManager).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        questionToManager = self.get_questionToManager(request, pk)
        if questionToManager == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user!= questionToManager.writer + 관리자가 아니면
            questionToManager.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentToQuestionViewWithQuestionPK(APIView):
    def get(self, request, pk):
        commentToQuestion = CommentToQuestion.objects.filter(QuestionToManager_id=pk)
        if (not commentToQuestion.questionToManager.isPrivate) or \
                (request.user == commentToQuestion.questionToManager.writer and request.user.is_authenticated) or \
                (request.user.is_staff and request.use):
            serializer = CommentToQuestionSerializer(commentToQuestion, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        if request.user.is_authenticated:
            if QuestionToManager.objects.get(pk=pk).writer != request.user or not(request.user.is_staff):  # True 자리에 관리자가 아니면 ? 로직 넣기
                return Response(status=status.HTTP_401_UNAUTHORIZED)


            commentToQuestion = CommentToQuestion.objects.create(
            writer=request.user,
            content=request.data["content"],
            questionToManager_id=pk,
            commentToQuestion_id=request.data["commentToQuestion"]
        )
            serializer = CommentToQuestionSerializer(commentToQuestion)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentToQuestionViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈

    def get_QuestionToManager(self, request, pk):
        try:
            commentToQuestion = CommentToQuestion.objects.get(pk=pk)
            if (not commentToQuestion.questionToManager.isPrivate) or (
                    request.user == commentToQuestion.questionToManager.writer and request.user.is_authenticated) \
                    or (request.user.is_staff and request.user):  # True대신에 관리자 로직 넣을것
                return commentToQuestion
            else:
                return None
        except commentToQuestion.DoesNotExist:
            return None

    def get(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(pk)
        if commentToQuestion == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CommentToQuestionSerializer(commentToQuestion)
            return Response(serializer.data)

    def put(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(pk)
        if commentToQuestion == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user != commentToQuestion.writer  or !관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # 바꿀 게 하나밖에 없어서 serializer 안 쓰고 그냥 객체에 직접 접근함.
        commentToQuestion.content = request.data["content"]
        commentToQuestion.save()

        return Response(CommentToQuestionSerializer(commentToQuestion).data)

    def delete(self, request, pk):
        commentToQuestion = self.get_commentToQuestion(pk)
        if commentToQuestion == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user != commentToQuestion.writer  or !관리자
            commentToQuestion.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class FeedbackToManagerView(APIView):

    def get(self, request):
        if not(request.user.is_authenticated and request.user.is_staff):  # 관리자가 아니라면
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        feedbackToManager = FeedbackToManager.objects.all()
        serializer = FeedbacksToManagerSerializer(feedbackToManager, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not(request.user and request.user.is_authenticated):  # 로그인 인증
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedbackToManagerSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            serializer.save(writer=request.user)  # 로그인 안하면 지금 오류남
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 수정기능 불필요해서 put 구현 안 함.
class FeedbackToManagerViewWithPk(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get_feedbackToManager(self, pk):
        try:
            feedbackToManager = FeedbackToManager.objects.get(pk=pk)
            return feedbackToManager
        except FeedbackToManager.DoesNotExist:
            return None

    def get(self, request, pk):
        if False:  # 관리자가 아니라면
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        feedbackToManager = self.get_feedbackToManager(pk)
        if feedbackToManager == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FeedbackToManagerSerializer(feedbackToManager)
            return Response(serializer.data)

    def delete(self, request, pk):
        feedbackToManager = self.get_feedbackToManager(pk)
        if feedbackToManager == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # 관리자 인증 로직
            feedbackToManager.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
