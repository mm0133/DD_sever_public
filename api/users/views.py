from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.models import CustomProfile
from api.users.serializer import CustomProfileSerializer, CustomProfileSerializerForOwner, CustomProfileSerializerForPut


@api_view(['GET'])
def get_Profile(request, nickname):
    profile = CustomProfile.objects.get(nickname=nickname)
    serializer = CustomProfileSerializer(profile, context={"user":request.user})
    return Response(serializer.data)

@api_view(['POST'])
def post_Profile(request, nickname):

    #이미 프로필있는경우 안됨
    if CustomProfile.objects.get(user=request.user):
        return Response(status.HTTP_400_BAD_REQUEST)

    profile=CustomProfile.objects.create(
        user=request.user,
        nickname=request.data["nickname"],
        phoneNumber=request.data["phoneNumber"],
        email=request.data["email"]
    )
    serializer=CustomProfileSerializerForOwner(profile).data
    return Response(data=serializer.data, status=status.HTTP_200_OK)



class CustomProfileView(APIView):

    # 자기자신 아니면 NotFound
    def get_CustomProfile(self, request, pk):
        try:
            customProfile = CustomProfile.objects.get(pk=pk)
            if request.user != customProfile.user:
                return None
            return customProfile
        except customProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        customProfile = self.get_customProfile(pk)
        if customProfile ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CustomProfileSerializerForOwner(customProfile)
            return Response(serializer.data)


    def put(self, request, pk):
        customProfile = self.get_customProfile(pk)
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


    def delete(self, request, pk):
        customProfile = self.get_customProfile(pk)
        if customProfile == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            customProfile.delete()
            return Response(status=status.HTTP_200_OK)

