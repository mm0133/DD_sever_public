from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from annoying.functions import get_object_or_None

from api.users.models import CustomProfile, Team, TeamInvite
from api.users.serializer import CustomProfileSerializer, MyCustomProfileSerializer, \
    CustomProfileSerializerForChange, TeamsSerializer, TeamSerializer, TeamsSerializerForPost, \
    TeamInviteSerializerForAccept, ChangePasswordSerializer, UserCreateSerializer, TeamInviteSerializer, \
    ProfileBasicInformationSerializer
from config.customExceptions import get_value_or_error
from config.customExceptions import get_object_or_404_custom
from config.utils import DDCustomListAPiView


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_myPage(request):
    profile = CustomProfile.objects.get(user=request.user)
    serializer = MyCustomProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
def get_profile(request, nickname):
    profile = get_object_or_404_custom(CustomProfile, nickname=nickname)
    serializer = CustomProfileSerializer(profile)
    return Response(serializer.data)


class CustomProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_customProfile(self, request):
        customProfile = get_object_or_404_custom(CustomProfile, user=request.user)
        return customProfile

    # 개인정보 수정으로 갔을 때 현재 상태 띄우려면 본인이 수정할 수 있는 정보에 대한 compact 한 세트가 있으면 좋음.
    # 그래서 MyCustomProfileSerializer 와 달리 적은 항목만 리턴하는 serializer  쓰는 것이다.
    def get(self, request):
        customProfile = self.get_customProfile(request)
        # MyCustomProfileSerializer 와 다른 점은 그냥 수정용이라는 것
        serializer = CustomProfileSerializerForChange(customProfile)
        return Response(serializer.data)

    def post(self, request):
        if get_object_or_None(CustomProfile, user=request.user):
            return Response(f"{request.user.username}'s profile already exits.", status=status.HTTP_403_FORBIDDEN)

        serializer = CustomProfileSerializerForChange(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save(user=request.user)
            image = get_object_or_None(request.data, "image")
            if image:
                serializer.save(smallImage=image)
            else:
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        customProfile = self.get_customProfile(request)

        serializer = CustomProfileSerializerForChange(customProfile, data=request.data, partial=True)
        if serializer.is_valid():
            image = get_object_or_None(request.data, "image")
            if image:
                serializer.save(smallImage=image)
            else:
                serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_teams(request, nickname):
    user = get_object_or_404_custom(CustomProfile, nickname=nickname).user
    teams = user.teams
    serializer = TeamsSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_team(request):
    serializer = TeamsSerializerForPost(data=request.data, context={"user": request.user})
    if serializer.is_valid():
        serializer.save(representative=request.user, members=(request.user,))
        image = get_object_or_None(request.data, "image")
        if image:
            serializer.save(smallImage=image)
        else:
            serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamViewWithTeamName(APIView):
    def get(self, request, teamName):
        team = get_object_or_404_custom(Team, name=teamName)
        serializer = TeamSerializer(team, context={"user": request.user})
        return Response(data=serializer.data)

    def delete(self, request, teamName):
        team = get_object_or_404_custom(Team, name=teamName)

        if team.representative == request.user or request.user.is_staff:
            team.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TeamInviteListView(DDCustomListAPiView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TeamInvite.objects.all().order_by('-id')
    serializer_class = TeamInviteSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'representative__customProfile__nickname')
    ordering_fields = ('name', 'id')

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            rawQueryset = self.get_queryset()
        else:
            rawQueryset = self.get_queryset().filter(Q(team__representative=request.user) | Q(invitee=request.user))

        queryset = self.filter_queryset(rawQueryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TeamInviteSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = TeamInviteSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_invite_send(request, teamName):
    team = get_object_or_404_custom(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    invitingMessage = get_object_or_None(request.data, "invitingMessage")
    member = get_object_or_404_custom(CustomProfile, nickname=memberNickname).user

    if not (team.representative == request.user or request.user.is_staff):
        return Response(f"당신은 팀 {teamName}'의 대표도 아니고 관리자도 아닙니다. 초대 요청을 보낼 수 업습니다.",
                        status=status.HTTP_401_UNAUTHORIZED)

    if memberNickname == request.user.customProfile.nickname:
        return Response("스스로를 초대할 수 없습니다.", status=status.HTTP_403_FORBIDDEN)
    elif member in team.members.all():
        return Response(f"멤버 {memberNickname}는 이미 팀 {teamName}의 멤버입니다. 초대할 수 없습니다.",
                        status=status.HTTP_403_FORBIDDEN)
    elif get_object_or_None(TeamInvite, team=team, invitee=member):
        teamInvite = get_object_or_None(TeamInvite, team=team, invitee=member)
        # 아직 수락/거절 안 했을 때
        if not teamInvite.isFinished:
            return Response(f"당신은 {memberNickname}을 to team {teamName}에 이미 초대했습니다. ",
                            status=status.HTTP_403_FORBIDDEN)
        # 이미 거절했는데 다시 초대했을 때
        else:
            teamInvite.isFinished = False
            teamInvite.invitingMessage = invitingMessage
            teamInvite.save()
            return Response(status=status.HTTP_200_OK)

    TeamInvite.objects.create(
        team=team,
        invitee=member,
        invitingMessage=invitingMessage
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_invite_accept(request, teamName):
    team = get_object_or_404_custom(Team, name=teamName)
    teamInvite = get_object_or_404_custom(TeamInvite, team=team, invitee=request.user)

    if not (teamInvite.invitee == request.user or request.user.is_staff):
        return Response(f"당신은 팀 {teamName}'의 초대를 받지 않았고 관리자도 아닙니다. 초대를 수락할 수 없습니다.",
                        status=status.HTTP_401_UNAUTHORIZED)

    # 이렇게 해야 JS의 true/false 를 python 의 true/false 로 알아들을 수 있음.
    serializer = TeamInviteSerializerForAccept(teamInvite, data=request.data)
    if serializer.is_valid():
        serializer.save()

        if serializer.data["isAccepted"]:
            team.members.add(teamInvite.invitee)

        teamInvite.isFinished = True
        teamInvite.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_invite_cancel(request, teamName):
    team = get_object_or_404_custom(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    member = get_object_or_404_custom(CustomProfile, nickname=memberNickname).user
    teamInvite = get_object_or_404_custom(TeamInvite, team=team, invitee=member)
    if team.representative == request.user or request.user.is_staff:
        teamInvite.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(f"당신은 팀 {teamName}'의 대표도 관리자도 아닙니다. 멤버 초대 요청을 취소할 수 없습니다.",
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_delete(request, teamName):
    team = get_object_or_404_custom(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    member = get_object_or_404_custom(CustomProfile, nickname=memberNickname).user
    # 1. 관리자 2. 팀의 대표가 멥버를 강퇴 3. 팀 멤버가 자진 탈퇴
    if request.user.is_staff or team.representative == request.user or member == request.user:
        if member == team.representative:
            if team.members.exclude(id=request.user.id):
                team.representative = list(team.members.exclude(id=request.user.id))[0]
                team.save()
                team.members.remove(member)
            else:
                team.delete()
        else:
            team.members.remove(member)

        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_representative(request, teamName):
    team = get_object_or_404_custom(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    if team.representative == request.user or request.user.is_staff:
        member = get_object_or_404_custom(CustomProfile, nickname=memberNickname).user
        team.representative = member
        team.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    model = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    teams = Team.objects.filter(representative=request.user)
    if teams:
        for team in teams:
            if team.members.exclude(id=request.user.id):
                team.representative = team.members.exclude(id=request.user.id)[0]
                team.save()
            else:
                team.delete()
    request.user.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['delete'])
@permission_classes([permissions.IsAdminUser])
def delete_user_pk(request, pk):
    user = get_object_or_404_custom(User, pk=pk)
    teams = Team.objects.filter(representative=user)
    for team in teams:
        if team.members.exclude(id=user.id):
            team.representative = team.members.exclude(id=request.user.id)[0]
            team.save()
        else:
            team.delete()
    user.delete()
    Response(status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("oldPassword")):
                return Response({"oldPassword": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("newPassword"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def HasCustomProfile(request):
    if get_object_or_None(CustomProfile, user=request.user):
        hasProfile = True
    else:
        hasProfile = False
    data = {"hasProfile": hasProfile}
    return Response(data)


@api_view(['GET'])
def check_is_me_staff(request):
    data = {"isStaff": request.user.is_staff}
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def myBasicInformation(request):
    customProfile = request.user.customProfile
    serializer = ProfileBasicInformationSerializer(customProfile)
    return Response(data=serializer.data, status=status.HTTP_401_UNAUTHORIZED)
