from annoying.functions import get_object_or_None
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.contests.models import Contest, ContestFile, ContestParticipantAnswer
from api.contests.serializer import ContestsSerializer, ContestSerializer, ContestFileSerializer, \
    ContestParticipantAnswerSerializer, ContestParticipantAnswersSerializer
from api.users.models import Team
from config.customExceptions import get_value_or_error
from config.customPermissions import IsGetRequestOrAdminUser, IsGetRequestOrAuthenticated, \
    IsGetRequestOrTeamRepresentativeOrOwner


class ContestView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request):
        contest = Contest.objects.all()
        serializer = ContestsSerializer(contest, many=True, context={'user': request.user})
        # contex={'request':requuest}로 request객체 받아서 쓸수도 있음
        return Response(serializer.data)

    def post(self, request):
        serializer = ContestSerializer(data=request.data, context={'user': request.user}),
        if serializer.is_valid():  # validation 로직 손보기
            # writer가 null=True이기 때문에 프론트에서 넣어주지 않아도 .is_valid에서 에러가 나지 않는다.
            # 그래서 밑에서 witer로 넣어주는 것이다.
            serializer.save(writer=request.useif)  # 일단 임시로 안 넣어줌. # 로그인 안하면 지금 오류남
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
        if contest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestSerializer(contest, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        contest = self.get_contest(pk)
        if contest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ContestSerializer(contest, data=request.data, partial=True, context={'user': request.user})
        if serializer.is_valid():  # validate 로직 검토
            contest = serializer.save()
            return Response(ContestSerializer(contest, context={'user': request.user}).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contest = self.get_contest(pk)
        if contest is None:
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
        serializer = ContestFileSerializer(contestFile, context={'user': request.user}, many=True)
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
        serializer = ContestFileSerializer(contestFile, context={'user': request.user}, many=True)
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


class ContestParticipantAnswerViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    # 내림차순정렬
    def get(self, request, pk):
        contestParticipantAnswer = ContestParticipantAnswer.objects.filter(contest_id=pk).order_by('-accuracy')
        print(contestParticipantAnswer)
        serializer = ContestParticipantAnswersSerializer(contestParticipantAnswer, context={'user': request.user},
                                                         many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        teamName = get_object_or_None(request.data, "teamName")
        file = get_value_or_error(request.data, "file")
        #팀제출
        if teamName:
            team = get_object_or_404(Team, name=teamName)
            if not (team.representative == request.user or not request.user.is_staff):
                return Response("팀의 대표만 답 제출을 할 수 있습니다.", status=status.HTTP_401_UNAUTHORIZED, )

            members = team.members.all()
            for member in members:
                nickname = member.customProfile.nickname
                if ContestParticipantAnswer.objects.filter(user=member, contest_id=pk):
                    return Response(f'팀원 {member.customProfile.nickname}님이 이미 답안을 제출 했습니다.',status=status.HTTP_400_BAD_REQUEST)

                answers = ContestParticipantAnswer.objects.filter(contest_id=pk)
                for answer in answers:
                    if answer.team:
                        if nickname in answer.teamMembers:
                            return Response(f'팀원 {nickname}님이 {answer.name}팀으로 이미 참가했습니다.',status=status.HTTP_400_BAD_REQUEST)


            teamMembers = []
            for member in team.members.all():
                teamMembers.append(member.customProfile.nickname)

            contestParticipantAnswer = ContestParticipantAnswer.objects.create(
                isTeam=True,
                team=team,
                name=teamName,
                teamMembers=teamMembers,
                contest_id=pk,
                file=file
            )
        #개인제출
        else:
            if ContestParticipantAnswer.objects.filter(user=request.user, contest_id=pk):
                return Response("이미 답안 제출했습니다.", status=status.HTTP_400_BAD_REQUEST)

            answers = ContestParticipantAnswer.objects.filter(contest_id=pk)
            for answer in answers:
                if answer.team:
                    if request.user.customProfile.nickname in answer.teamMembers:
                        return Response(f'이미 {answer.name}팀으로 참가했습니다.', status=status.HTTP_400_BAD_REQUEST)

            contestParticipantAnswer = ContestParticipantAnswer.objects.create(
                isTeam=False,
                user=request.user,
                name=request.user.customProfile.nickname,
                contest_id=pk,
                file=file
            )
        # 정확도 계산 로직 넣어야함
        contestParticipantAnswer.accuracy = contestParticipantAnswer.calculateAccuracy()
        contestParticipantAnswer.save()
        serializer = ContestParticipantAnswerSerializer(contestParticipantAnswer, context={'user': request.user})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ContestParticipantAnswerViewWithPK(APIView):
    permission_classes = [IsGetRequestOrTeamRepresentativeOrOwner]

    def get_contestParticipantAnswer(self, pk):
        try:
            contestParticipantAnswer = ContestParticipantAnswer.objects.get(pk=pk)
            self.check_object_permissions(self.request, contestParticipantAnswer)
            return contestParticipantAnswer
        except contestParticipantAnswer.DoesNotExist:
            return None

    def get(self, request, pk):
        contestParticipantAnswer = get_object_or_404(ContestParticipantAnswer, pk)
        if not (request.user.is_authenticated or request.user in contestParticipantAnswer.teamMembers.all()):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            serializer = ContestParticipantAnswerSerializer(contestParticipantAnswer, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        contestParticipantAnswer = self.get_contestParticipantAnswer(pk)
        if contestParticipantAnswer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.data['file']:
            contestParticipantAnswer.file = request.data['file']
            contestParticipantAnswer.save()

            return Response(
                ContestParticipantAnswerSerializer(contestParticipantAnswer, context={'user': request.user}).data)

    def delete(self, request, pk):
        contestParticipantAnswer = self.get_contestParticipantAnswer(pk)
        if contestParticipantAnswer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contestParticipantAnswer.delete()
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
