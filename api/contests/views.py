from django.shortcuts import get_object_or_404, redirect, render

from annoying.functions import get_object_or_None
from api.contests.models import Contest, ContestFile, ContestParticipantAnswer
from api.contests.serializer import (ContestFileSerializer,
                                     ContestParticipantAnswerSerializer,
                                     ContestParticipantAnswersSerializer,
                                     ContestSerializer, ContestsSerializer, ContestSerializerForPost)
from api.users.models import Team
from config.customExceptions import get_value_or_error
from config.customPermissions import (IsGetRequestOrAdminUser,
                                      IsGetRequestOrAuthenticated,
                                      IsGetRequestOrTeamRepresentativeOrOwner)
# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


class ContestView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request):
        contest = Contest.objects.all()
        serializer = ContestsSerializer(contest, many=True, context={'user': request.user})
        # context ={'request':request}로 request 객체 받아서 쓸수도 있음
        return Response(serializer.data)

    def post(self, request):
        serializer = ContestSerializerForPost(data=request.data, context={'user': request.user})
        if serializer.is_valid():  # validation 로직 손보기
            # writer 가 null=True 이기 때문에 프론트에서 넣어주지 않아도 .is_valid 에서 에러가 나지 않는다.
            # 그래서 밑에서 writer 로 넣어주는 것이다.
            serializer.save(writer=request.user)  # 일단 임시로 안 넣어줌. # 로그인 안하면 지금 오류남
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        serializer = ContestSerializer(contest, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)

        serializer = ContestSerializer(contest, data=request.data, partial=True, context={'user': request.user})
        if serializer.is_valid():
            contest = serializer.save()
            return Response(ContestSerializer(contest, context={'user': request.user}).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        contest.delete()
        return Response(status=status.HTTP_200_OK)


class ContestFileViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        contestFiles = ContestFile.objects.filter(contest=contest)

        serializer = ContestFileSerializer(contestFiles, context={'user': request.user}, many=True)
        return Response(serializer.data)

    # 다중업로드 가능!
    def post(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)

        files = dict(request.data.lists())['file']

        for file in files:
            ContestFile.objects.create(
                contest=contest,
                file=file,
            )

        contestFiles = ContestFile.objects.filter(contest=contest)

        serializer = ContestFileSerializer(contestFiles, context={'user': request.user}, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        contestFiles = ContestFile.objects.filter(contest=contest)
        contestFiles.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def DeleteContestFileWithPK(request, pk):
    if not request.user.is_staff:
        Response(status=status.HTTP_403_FORBIDDEN)

    contestFile = get_object_or_404(ContestFile, pk=pk)
    contestFile.delete()
    return Response(status=status.HTTP_200_OK)


class ContestParticipantAnswerViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    # 내림차순정렬
    def get(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        contestParticipantAnswer = ContestParticipantAnswer.objects.filter(contest=contest).order_by('-accuracy')
        serializer = ContestParticipantAnswersSerializer(contestParticipantAnswer, context={'user': request.user},
                                                         many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        teamName = get_object_or_None(request.data, "teamName")
        file = get_value_or_error(request.data, "file")
        # 팀제출
        if teamName:
            team = get_object_or_404(Team, name=teamName)
            if not (team.representative == request.user or request.user.is_staff):
                return Response("팀의 대표만 답 제출을 할 수 있습니다.", status=status.HTTP_401_UNAUTHORIZED, )

            members = team.members.all()
            for member in members:
                nickname = member.customProfile.nickname
                if ContestParticipantAnswer.objects.filter(user=member, contest=contest):
                    return Response(f'팀원 {member.customProfile.nickname}님이 이미 답안을 제출 했습니다.',
                                    status=status.HTTP_400_BAD_REQUEST)

                answers = ContestParticipantAnswer.objects.filter(contest=contest)
                for answer in answers:
                    if answer.team:
                        if nickname in answer.teamMembers:
                            return Response(f'팀원 {nickname}님이 {answer.name}팀으로 이미 참가했습니다.',
                                            status=status.HTTP_400_BAD_REQUEST)

            teamMembers = []
            for member in team.members.all():
                teamMembers.append(member.customProfile.nickname)

            contestParticipantAnswer = ContestParticipantAnswer.objects.create(
                isTeam=True,
                team=team,
                name=teamName,
                teamMembers=teamMembers,
                contest=contest,
                file=file
            )
        # 개인제출
        else:
            if ContestParticipantAnswer.objects.filter(user=request.user, contest=contest):
                return Response("이미 답안을 제출했습니다.", status=status.HTTP_400_BAD_REQUEST)

            answers = ContestParticipantAnswer.objects.filter(contest=contest)
            for answer in answers:
                if answer.team:
                    if request.user.customProfile.nickname in answer.teamMembers:
                        return Response(f'이미 {answer.name}팀으로 참가했습니다.', status=status.HTTP_400_BAD_REQUEST)

            contestParticipantAnswer = ContestParticipantAnswer.objects.create(
                isTeam=False,
                user=request.user,
                name=request.user.customProfile.nickname,
                contest=contest,
                file=file
            )
        contestParticipantAnswer.accuracy = contestParticipantAnswer.calculateAccuracy()
        contestParticipantAnswer.save()
        serializer = ContestParticipantAnswerSerializer(contestParticipantAnswer, context={'user': request.user})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ContestParticipantAnswerViewWithPK(APIView):
    # get 요청은 팀 멤버만 볼 수 있음. 별도로 if 문을 get 에서 추가해줘서 멤버만 볼 수 있는 로직 구현.
    # 그 외에 수정, 삭제는
    permission_classes = [IsGetRequestOrTeamRepresentativeOrOwner]

    def get_contestParticipantAnswer(self, pk):
        contestParticipantAnswer = get_object_or_404(ContestParticipantAnswer, pk=pk)
        self.check_object_permissions(self.request, contestParticipantAnswer)
        return contestParticipantAnswer

    def get(self, request, pk):
        contestParticipantAnswer = get_object_or_404(ContestParticipantAnswer, pk=pk)
        if contestParticipantAnswer.team:
            if request.user.customProfile.nickname not in contestParticipantAnswer.teamMembers:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not (request.user and request.user.is_authenticated and request.user == contestParticipantAnswer.user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestParticipantAnswerSerializer(contestParticipantAnswer, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        contestParticipantAnswer = self.get_contestParticipantAnswer(pk)
        file = get_value_or_error(request.data, 'file')
        contestParticipantAnswer.file.delete()
        contestParticipantAnswer.file = file
        contestParticipantAnswer.save()
        return Response(
            ContestParticipantAnswerSerializer(contestParticipantAnswer, context={'user': request.user}).data)

    def delete(self, request, pk):
        contestParticipantAnswer = self.get_contestParticipantAnswer(pk)
        contestParticipantAnswer.delete()
        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestScrap(request, pk):
    contest = get_object_or_404(Contest, pk=pk)
    if contest not in request.user.customProfile.contestScraps.all():
        request.user.customProfile.contestScraps.add(contest)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.contestScraps.remove(contest)
        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestParticipantAnswerLike(request, pk):
    contestParticipantAnswer = get_object_or_404(ContestParticipantAnswer, pk=pk)
    if contestParticipantAnswer not in request.user.contestAnswerLikes.all():
        request.user.contestAnswerLikes.add(contestParticipantAnswer)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.contestAnswerLikes.remove(contestParticipantAnswer)
        return Response(status=status.HTTP_200_OK)
