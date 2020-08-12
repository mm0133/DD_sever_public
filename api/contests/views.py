from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.contests.models import Contest, ContestFile, ContestUserAnswer
from api.contests.serializer import ContestsSerializer, ContestSerializer, ContestFileSerializer, \
    ContestUserAnswerSerializer
from config.customPermissions import IsGetRequestOrAdminUser, IsGetRequestOrAuthenticated, IsWriterOrAdminUser


class ContestView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request):
        contest = Contest.objects.all()
        serializer = ContestsSerializer(contest, many=True, context={'user': request.user})
        # contex={'request':requuest}로 request객체 받아서 쓸수도 있음
        return Response(serializer.data)

    def post(self, request):
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            # writer가 null=True이기 때문에 프론트에서 넣어주지 않아도 .is_valid에서 에러가 나지 않는다.
            # 그래서 밑에서 witer로 넣어주는 것이다.
            serializer.save(writer=request.user)  # 일단 임시로 안 넣어줌. # 로그인 안하면 지금 오류남
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get_contest(self, pk):
        try:
            contest = get_object_or_404(Contest, pk=pk)
            self.check_object_permissions(self.request, contest)
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
        contest.delete()
        return Response(status=status.HTTP_200_OK)



class ContestFileViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        try:
            contestFile = ContestFile.objects.filter(contest_id=pk)
        except contestFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ContestFileSerializer(contestFile, many=True)
        return Response(serializer.data)

    # 다중업로드 가능!
    def post(self, request, pk):

        files = dict((request.data).lists())['file']

        for file in files:
            print(file)
            contestFile = ContestFile.objects.create(
                contest_id=pk,
                file=file,
            )

        contestFile = ContestFile.objects.filter(contest_id=pk)
        serializer = ContestFileSerializer(contestFile, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            contestFile = ContestFile.objects.filter(contest_id=pk)
        except contestFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contestFile.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def DeleteContestFileWithPK(request, pk):
    if not request.user.is_staff:
        Response(status=status.HTTP_403_FORBIDDEN)

    try:
        contestFile = ContestFile.objects.get(pk=pk)
    except contestFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    contestFile.delete()
    return Response(status=status.HTTP_200_OK)


class ContestUserAnswerViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    # 내림차순정렬
    def get(self, request, pk):
        contestUserAnswer = ContestUserAnswer.objects.filter(contest_id=pk).order_by('-accuracy')
        serializer = ContestUserAnswerSerializer(contestUserAnswer, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        contestUserAnswer = ContestUserAnswer.objects.create(
            writer=request.user,
            contest_id=pk,
            file=request.data['file']
        )
        # 정확도 계산 로직 넣어야함
        contestUserAnswer.accuracy = contestUserAnswer.calculateAccuracy()
        contestUserAnswer.save()
        serializer = ContestUserAnswerSerializer(contestUserAnswer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ContestUserAnswerViewWithPK(APIView):
    permission_classes = [IsWriterOrAdminUser]

    def get_contestUserAnswer(self, pk):
        try:
            contestUserAnswer = ContestUserAnswer.objects.get(pk=pk)
            self.check_object_permissions(self.request, contestUserAnswer)
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

        serializer = ContestUserAnswerSerializer(contestUserAnswer, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            contestUserAnswer = serializer.save()
            return Response(ContestUserAnswerSerializer(contestUserAnswer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestUserAnswer = self.get_contestUserAnswer(pk)
        if contestUserAnswer == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contestUserAnswer.delete()
        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestScrap(request, pk):
    contest = get_object_or_404(Contest, pk=pk)
    if contest in request.user.customProfile.contestScraps:
        request.user.customProfile.debateScraps.add(contest)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.debateScraps.remove(contest)
        return Response(status=status.HTTP_200_OK)
