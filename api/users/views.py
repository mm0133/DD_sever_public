from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import CustomProfile, Team, TeamInvite
from api.users.serializer import CustomProfileSerializer, CustomProfileSerializerForOwner, \
    CustomProfileSerializerForPut, MyCustomProfileSerializer, TeamsSerializer, TeamSerializer
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
        serializer = CustomProfileSerializerForOwner(customProfile)
        return Response(serializer.data)

    def post(self, request):

        if get_object_or_None(CustomProfile, user=request.user):
            raise DDCustomException(f"{request.user.username}'s profile already exits.")

        profile = CustomProfile.objects.create(
            user=request.user,
            nickname=get_value_or_error(request.data, "nickname"),
            phoneNumber=get_value_or_error(request.data, "phoneNumber"),
            email=get_value_or_error(request.data, "email")
        )
        serializer = CustomProfileSerializerForOwner(profile).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def put(self, request):
        customProfile = self.get_customProfile(request)

        serializer = CustomProfileSerializerForPut(customProfile, data=request.data, partial=True)
        if serializer.is_valid():
            customProfile = serializer.save()
            if get_object_or_None(request.data, "image"):
                customProfile.smallImage = request.data["image"]
                customProfile.save()
            # 파일 용량낮춰서 저장하기. image 는 자기 프로필에가면 조금 크게나오는 사진, smallImage 는 댓글 옆에 작은사진
            serializer = CustomProfileSerializerForOwner(customProfile)
            return Response(serializer.data)
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
    team = Team.objects.create(
        name=request.data["name"],
        representative=request.user,
    )
    team.members.add(request.user)
    serializer = TeamSerializer(team, context={"user": request.user})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class TeamViewWithTeamName(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    if memberNickname == request.user.customProfile.nickname:
        return Response("you can't invite yourself!", status=status.HTTP_403_FORBIDDEN)
    if team.representative == request.user or request.user.is_staff:
        member = get_object_or_404(CustomProfile, nickname=memberNickname).user
        TeamInvite.objects.create(
            inviter=request.user,
            invitee=member,
            invitingMessage=invitingMessage
        )
        return Response(status=status.HTTP_200_OK)
    return Response(f"you are neither team {teamName}'s representative nor staff user!",
                    status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_invite_accept(request, teamName):
    team = get_object_or_404(Team, name=teamName)
    isAccepted = get_value_or_error(request.data, "isAccepted")
    teamInvite = get_object_or_404(TeamInvite, inviter=team.representative, invitee=request.user)
    if teamInvite.invitee == request.user or request.user.is_staff:
        if isAccepted:
            team.members.add(teamInvite.invitee)
            teamInvite.isAccepted = True

        teamInvite.isFinished = True
        teamInvite.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(f"you are neither team {teamName}'s invitee nor staff user!",
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
