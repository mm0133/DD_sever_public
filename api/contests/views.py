from django.db.models import Count

from annoying.functions import get_object_or_None

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.contests.models import Contest, ContestFile, ContestParticipantAnswer
from api.contests.serializer import (ContestFileSerializer,
                                     ContestParticipantAnswerSerializer,
                                     ContestParticipantAnswersSerializer,
                                     ContestSerializer, ContestsSerializer, ContestSerializerForPost)
from api.users.models import Team
from config.customExceptions import get_value_or_error, get_object_or_404_custom
from config.customPermissions import (IsGetRequestOrAdminUser,
                                      IsGetRequestOrAuthenticated,
                                      IsGetRequestOrTeamRepresentativeOrOwner)
from config.utils import pagination_with_pagesize


class ContestListView(generics.ListAPIView):
    permission_classes = [IsGetRequestOrAdminUser]
    # queryset 은 해당 모델의 attribute 로만 filtering 이 가능하다. model function 같은 걸로 filtering 못 한다.
    # 그래서 아래와 같이 annotate 로 queryset 에 participantNumber 를 달아주고, 그 걸로 ordering(즉 filtering) 을 하게 하면 된다.
    queryset = Contest.objects.all().order_by('-id').annotate(participantNumber=Count('participantAnswer'))
    serializer_class = ContestsSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'subtitle')
    ordering_fields = ('participantNumber', 'id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestsSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = ContestsSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class ContestListNotPaginatedView(generics.ListAPIView):
    permission_classes = [IsGetRequestOrAdminUser]
    queryset = Contest.objects.all().order_by('-id').annotate(participantNumber=Count('participantAnswer'))
    serializer_class = ContestsSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'subtitle')
    ordering_fields = ('participantNumber', 'id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ContestsSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class ContestCreateView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def post(self, request):
        serializer = ContestSerializerForPost(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            contest = serializer.save(writer=request.user)
            returnSerializer = ContestSerializer(contest, context={'user': request.user})
            return Response(returnSerializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        contest = get_object_or_404_custom(Contest, pk=pk)
        serializer = ContestSerializer(contest, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        contest = get_object_or_404_custom(Contest, pk=pk)

        serializer = ContestSerializer(contest, data=request.data, partial=True, context={'user': request.user})
        if serializer.is_valid():
            contest = serializer.save()
            return Response(ContestSerializer(contest, context={'user': request.user}).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contest = get_object_or_404_custom(Contest, pk=pk)
        contest.delete()
        return Response(status=status.HTTP_200_OK)


class ContestFileViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        contest = get_object_or_404_custom(Contest, pk=pk)
        contestFiles = ContestFile.objects.filter(contest=contest)

        serializer = ContestFileSerializer(contestFiles, context={'user': request.user}, many=True)
        return Response(serializer.data)

    # 다중업로드 가능!
    def post(self, request, pk):
        contest = get_object_or_404_custom(Contest, pk=pk)

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
        contest = get_object_or_404_custom(Contest, pk=pk)
        contestFiles = ContestFile.objects.filter(contest=contest)
        contestFiles.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def DeleteContestFileWithPK(request, pk):
    if not request.user.is_staff:
        Response(status=status.HTTP_403_FORBIDDEN)

    contestFile = get_object_or_404_custom(ContestFile, pk=pk)
    contestFile.delete()
    return Response(status=status.HTTP_200_OK)


class ContestParticipantAnswerListViewWithContestPK(generics.ListAPIView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = ContestParticipantAnswer.objects.all().order_by('-accuracy')
    serializer_class = ContestParticipantAnswersSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('teamMembers', 'name')
    ordering_fields = ('accuracy', 'id')
    pagination_class = pagination_with_pagesize(30)

    def list(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset().filter(contest_id=pk))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestParticipantAnswersSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = ContestParticipantAnswersSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class ContestParticipantAnswerCreateViewWithContestPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def post(self, request, pk):
        contest = get_object_or_404_custom(Contest, pk=pk)
        teamName = get_object_or_None(request.data, "teamName")
        file = get_value_or_error(request.data, "file")
        # 팀제출
        if teamName:
            team = get_object_or_404_custom(Team, name=teamName)
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
        contestParticipantAnswer = get_object_or_404_custom(ContestParticipantAnswer, pk=pk)
        self.check_object_permissions(self.request, contestParticipantAnswer)
        return contestParticipantAnswer

    def get(self, request, pk):
        contestParticipantAnswer = get_object_or_404_custom(ContestParticipantAnswer, pk=pk)
        if contestParticipantAnswer.isTeam:
            if not request.user.is_authenticated:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            elif request.user.customProfile.nickname not in contestParticipantAnswer.teamMembers:
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
    contest = get_object_or_404_custom(Contest, pk=pk)
    if contest not in request.user.customProfile.contestScraps.all():
        request.user.customProfile.contestScraps.add(contest)
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        request.user.customProfile.contestScraps.remove(contest)
        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestParticipantAnswerLike(request, pk):
    contestParticipantAnswer = get_object_or_404_custom(ContestParticipantAnswer, pk=pk)
    if contestParticipantAnswer not in request.user.contestAnswerLikes.all():
        request.user.contestAnswerLikes.add(contestParticipantAnswer)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.contestAnswerLikes.remove(contestParticipantAnswer)
        return Response(status=status.HTTP_200_OK)
