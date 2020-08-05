from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import CustomProfile
from api.users.serializer import CustomProfileSerializer, CustomProfileSerializerForOwner, \
    CustomProfileSerializerForPut, MyCustomProfileSerializer


@api_view(['GET'])
def get_Profile(request, nickname):
    profile = CustomProfile.objects.get(nickname=nickname)
    if  request.user.customProfile.nickname == nickname: #본인 맞는지 인증
        serializer = MyCustomProfileSerializer(profile, context={"user":request.user})
    else:
        serializer = CustomProfileSerializer(profile, context={"user":request.user})
    return Response(serializer.data)


class CustomProfileView(APIView):

    # 자기자신 아니면 NotFound
    def get_CustomProfile(self, request):
        try:
            customProfile = CustomProfile.objects.get(user=request.user)
            if False: #본인인증관련 비밀번호한번더 입력? 이런거 있어야할듯
                return None
            return customProfile
        except customProfile.DoesNotExist:
            return None

    def get(self, request):
        customProfile = self.get_customProfile(request)
        if customProfile ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CustomProfileSerializerForOwner(customProfile)
            return Response(serializer.data)


    def post(self,request):

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
        if serializer.is_valid():#validate 로직 검토
            customProfile = serializer.save()
            if request.data["Image"]:
                customProfile.image=""
                customProfile.smallImage=""
            #파일 용량낮춰서 저장하기. image는 자기 프로필에가면 조금 크게나오는 사진, smallimage는 댓글 옆에 작은사진
            serializer=CustomProfileSerializerForOwner(customProfile)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
