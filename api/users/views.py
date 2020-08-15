from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import CustomProfile, Team, TeamInvite
from api.users.serializer import CustomProfileSerializer, MyCustomProfileSerializer, \
    CustomProfileSerializerForChange, TeamsSerializer, TeamSerializer, TeamsSerializerForPost, \
    TeamInviteSerializerForAccept
from config.customExceptions import DDCustomException, get_value_or_error
from annoying.functions import get_object_or_None


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_myPage(request):
    profile = CustomProfile.objects.get(user=request.user)
    serializer = MyCustomProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
def get_Profile(request, nickname):
    profile = get_object_or_404(CustomProfile, nickname=nickname)
    serializer = CustomProfileSerializer(profile)
    return Response(serializer.data)


class CustomProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_customProfile(self, request):
        customProfile = get_object_or_404(CustomProfile, user=request.user)
        if False:  # 비밀번호 한번 더 입력하는 url 로 리다이렉트시키기.
            return None
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
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_teams(request, nickname):
    user = get_object_or_404(CustomProfile, nickname=nickname).user
    teams = user.teams
    serializer = TeamsSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_team(request):
    serializer = TeamsSerializerForPost(data=request.data, context={"user": request.user})
    if serializer.is_valid():
        serializer.save(representative=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamViewWithTeamName(APIView):
    def get(self, request, teamName):
        team = get_object_or_404(Team, name=teamName)
        serializer = TeamSerializer(team, context={"user": request.user})
        return Response(data=serializer.data)

    def delete(self, request, teamName):
        team = get_object_or_404(Team, name=teamName)

        if team.representative == request.user or request.user.is_staff:
            team.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_invite(request, teamName):
    team = get_object_or_404(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    invitingMessage = get_object_or_None(request.data, "invitingMessage")
    member = get_object_or_404(CustomProfile, nickname=memberNickname).user

    if not (team.representative == request.user or request.user.is_staff):
        return Response(f"you are neither team {teamName}'s representative nor staff user!",
                        status=status.HTTP_401_UNAUTHORIZED)

    if memberNickname == request.user.customProfile.nickname:
        return Response("you can't invite yourself!", status=status.HTTP_403_FORBIDDEN)
    elif member in team.members.all():
        return Response(f"{memberNickname} is already team {teamName}'s member.", status=status.HTTP_403_FORBIDDEN)
    elif get_object_or_None(TeamInvite, team=team, invitee=member):
        teamInvite = get_object_or_None(TeamInvite, team=team, invitee=member)
        # 아직 수락/거절 안 했을 때
        if not teamInvite.isFnished:
            return Response(f"you already invited {memberNickname} to team {teamName} ",
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
    team = get_object_or_404(Team, name=teamName)
    teamInvite = get_object_or_404(TeamInvite, team=team, invitee=request.user)

    if not (teamInvite.invitee == request.user or request.user.is_staff):
        return Response(f"you are neither team {teamName}'s invitee nor staff user!",
                        status=status.HTTP_401_UNAUTHORIZED)

    # 이렇게 해야 JS의 true/false 를 python 의 true/false 로 알아들을 수 있음.
    serializer = TeamInviteSerializerForAccept(teamInvite, data=request.data, partial=True)
    if serializer.is_valid():
        if serializer.data.isAccepted:
            team.members.add(teamInvite.invitee)

    teamInvite.isFinished = True
    teamInvite.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_invite_cancel(request, teamName):
    team = get_object_or_404(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    member = get_object_or_404(CustomProfile, nickname=memberNickname).user
    teamInvite = get_object_or_404(TeamInvite, team=team, invitee=member)
    if team.representative == request.user or request.user.is_staff:
        teamInvite.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(f"you are neither team {teamName}'s representative nor staff user!",
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_delete(request, teamName):
    team = get_object_or_404(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    if team.representative == request.user or request.user.is_staff or \
            memberNickname == request.user.customProfile.nickname:
        member = get_object_or_404(CustomProfile, nickname=memberNickname).user
        if member == team.representative:
            if team.members.exclude(id=request.user.id):
                team.representative = team.members.exclude(id=request.user.id)[0]
                team.save()
                team.members.remove(member)
            else:
                team.delete()
        else:
            team.members.remove(member)

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_representative(request, teamName):
    team = get_object_or_404(Team, name=teamName)
    memberNickname = get_value_or_error(request.data, "memberNickname")
    if team.representative == request.user or request.user.is_staff:
        member = get_object_or_404(CustomProfile, nickname=memberNickname).user
        team.representative = member
        team.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['delete'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    teams = Team.objects.filter(representative=request.user)
    if teams:
        for team in teams:
            otherMembers = team.members.exclude(id=request.user.id)
            if otherMembers:
                team.representative = otherMembers[0]
                team.save()
            else:
                team.delete()
    request.user.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['delete'])
@permission_classes([permissions.IsAdminUser])
def delete_user_pk(request, pk):
    user = User.objects.get(pk=pk)
    teams = Team.objects.filter(representative=user)
    for team in teams:
        otherMembers = team.members.exclude(id=user.id)
        if otherMembers:
            team.representative = otherMembers[0]
            team.save()
        else:
            team.delete()
    user.delete()
    Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def password_check(request):
    pass
