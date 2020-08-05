from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.contests.models import Contest, ContestFile, ContestUserAnswer
from api.contests.serializer import ContestsSerializer, ContestSerializer, ContestFileSerializer, \
    ContestUserAnswerSerializer


class ContestView(APIView):

    def get(self, request):
        contest = Contest.objects.all()
        serializer = ContestsSerializer(contest, many=True, context={'user': request.user})
        # contex={'request':requuest}로 request객체 받아서 쓸수도 있음
        return Response(serializer.data)

    def post(self, request):
        if False:  # 관리자 인증필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            # writer가 null=True이기 때문에 프론트에서 넣어주지 않아도 .is_valid에서 에러가 나지 않는다.
            # 그래서 밑에서 witer로 넣어주는 것이다.
            serializer.save(writer=request.user)  # 로그인 안하면 지금 오류남
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestViewWithPk(APIView):

    def get_contest(self, pk):
        try:
            contest = Contest.objects.get(pk=pk)
            return contest
        except contest.DoesNotExist:
            return None

    def get(self, request, pk):
        contest = self.get_contest(pk)
        if contest == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestSerializer(contest)
            return Response(serializer.data)

    def put(self, request, pk):
        contest = self.get_contest(pk)
        if contest == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # 관리자가 아니면
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestSerializer(contest, data=request.data, partial=True, context={'user': request.user})
        if serializer.is_valid():  # validate 로직 검토
            contest = serializer.save()
            return Response(ContestSerializer(contest).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contest = self.get_contest(pk)
        if contest == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # 관리자면
            contest.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ContestFileViewWithContestPK(APIView):

    def get(self, pk):
        try:
            contestFile = ContestFile.objects.filter(contest_id=pk)
        except contestFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ContestFileSerializer(contestFile, many=True)
        return Response(serializer.data)

    # 다중업로드 기능(한 번에 여러 파일 제출) 확인해봐야함
    def post(self, request, pk):
        if False:  # 관리자 인증필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # 여러 개 한 꺼번에. 안 되면 그냥 for 문 돌리면 됨.
        serializer = ContestFileSerializer(data=request.data, many=True)
        if serializer.is_valid():  # validation 로직 손보기
            contest = Contest.objects.get(pk=pk)
            serializer.save(contest=contest)  # 되는지 확인해봐야함
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if False:  # 관리자가 아니라면
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            contestFile = ContestFile.objects.filter(contest_id=pk)
        except contestFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contestFile.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def DeleteContestFileWithPK(request, pk):
    if False:  # 관리자가 아니라면
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        contestFile = ContestFile.objects.get(pk=pk)
    except contestFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    contestFile.delete()
    return Response(status=status.HTTP_200_OK)


class ContestUserAnswerViewWithContestPK(APIView):
    # 내림차순정렬
    def get(self, request, pk):
        contestUserAnswer = ContestUserAnswer.objects.filter(contest_id=pk).order_by('-accuracy')
        serializer = ContestUserAnswerSerializer(contestUserAnswer, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        contestUserAnswer = ContestUserAnswer.objects.create(
            writer=request.user,
            contest_id=pk,
            file=request.data["file"],
        )
        # 정확도 계산 로직 넣어야함
        contestUserAnswer.accuracy = contestUserAnswer.calculateAccuracy()
        contestUserAnswer.save()
        serializer = ContestUserAnswerSerializer(contestUserAnswer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ContestUserAnswerViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈

    def get_contestUserAnswer(self, pk):
        try:
            contestUserAnswer = ContestUserAnswer.objects.get(pk=pk)
            return contestUserAnswer
        except contestUserAnswer.DoesNotExist:
            return None

    def get(self, request, pk):
        contestUserAnswer = self.get_contestUserAnswer(pk)
        if contestUserAnswer == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestUserAnswerSerializer(contestUserAnswer)
            return Response(serializer.data)

    def put(self, request, pk):
        contestUserAnswer = self.get_contestUserAnswer(pk)
        if contestUserAnswer == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestUserAnswerSerializer(contestUserAnswer, data=request.data, partial=True, )
        if serializer.is_valid():  # validate 로직 추가
            contestUserAnswer = serializer.save()
            return Response(ContestUserAnswerSerializer(contestUserAnswer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestUserAnswer = self.get_contestUserAnswer(pk)
        if contestUserAnswer == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == contestUserAnswer.writer  or 관리자
            contestUserAnswer.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
