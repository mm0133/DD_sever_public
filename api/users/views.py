from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import CustomProfile, Team
from api.users.serializer import CustomProfileSerializer, CustomProfileSerializerForOwner, \
    CustomProfileSerializerForPut, MyCustomProfileSerializer, TeamsSerializer, TeamSerializer


@api_view(['GET'])
def get_Profile(request, nickname):
    profile = CustomProfile.objects.get(nickname=nickname)
    serializer = CustomProfileSerializer(profile, context={"user": request.user})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_myPage(request):
    profile = CustomProfile.objects.get(user=request.user)
    serializer = MyCustomProfileSerializer(profile, context={"user": request.user})
    return Response(serializer.data)


class CustomProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_CustomProfile(self, request):
        try:
            customProfile = CustomProfile.objects.get(user=request.user)
            if False:  # 본인인증관련 비밀번호한번더 입력? 이런거 있어야할듯
                return None
            return customProfile
        except customProfile.DoesNotExist:
            return None

    def get(self, request):
        customProfile = self.get_customProfile(request)
        if customProfile == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CustomProfileSerializerForOwner(customProfile)
            return Response(serializer.data)

    def post(self, request):

        if CustomProfile.objects.get(user=request.user):
            return Response(status.HTTP_400_BAD_REQUEST)

        profile = CustomProfile.objects.create(
            user=request.user,
            nickname=request.data["nickname"],
            phoneNumber=request.data["phoneNumber"],
            email=request.data["email"]
        )
        serializer = CustomProfileSerializerForOwner(profile).data
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        customProfile = self.get_customProfile(request)
        if customProfile == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomProfileSerializerForPut(customProfile, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 검토
            customProfile = serializer.save()
            if request.data["Image"]:
                customProfile.smallImage = request.data["Image"]
                customProfile.save()
            # 파일 용량낮춰서 저장하기. image는 자기 프로필에가면 조금 크게나오는 사진, smallimage는 댓글 옆에 작은사진
            serializer = CustomProfileSerializerForOwner(customProfile)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_teams(request, nickname):
    user = CustomProfile.objects.get(nickname=nickname).user
    Teams = Team.objects.filter(id=user.id)
    serializer = TeamsSerializer(Teams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_team(request):
    team = Team.objects.create(
        name=request.data["name"],
        representative=request.user,
    )
    team.members.add(request.user)
    serializer = TeamSerializer(team)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class TeamViewWithTeamName(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_Team(self, request, teamName):
        try:
            team = Team.objects.get(name=teamName)
            return team
        except team.DoesNotExist:
            return None

    def get(self, request, teamName):
        team = self.get_team(request, teamName)
        if team == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = TeamSerializer(team)
            return Response(serializer.data)

    def delete(self, request, teamName):
        team = self.get_team(request, teamName)
        if team == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if team.representative == request.user or request.user.is_staff:
            team.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_add(request, teamName):
    try:
        team = Team.objects.get(name=teamName)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if team.representative == request.user or request.user.is_staff:
        member = CustomProfile.objects.get(nickname=request.data["memberNickname"]).user
        team = Team.objects.get(name=teamName)
        team.members.add(member)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def member_delete(request, teamName):
    try:
        team = Team.objects.get(name=teamName)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if team.representative == request.user or request.user.is_staff or request.data[
        "memberNickname"] == request.user.customProfile.nickname:
        member = CustomProfile.objects.get(nickname=request.data["memberNickname"]).user
        team = Team.objects.get(name=teamName)
        if member == team.representative:
            if team.members.exclude(id=request.user.id):
                team.representative = team.members.exclude(id=request.user.id)[0]
                team.save()
            else:
                team.delete()
        team.members.remove(member)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_representative(request, teamName):
    try:
        team = Team.objects.get(name=teamName)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if team.representative == request.user or request.user.is_staff:
        member = CustomProfile.objects.get(nickname=request.data["memberNickname"]).user
        team = Team.objects.get(name=teamName)
        team.representative = member
        team.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['delete'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    teams = Team.objects.filter(representative=request.user)
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
