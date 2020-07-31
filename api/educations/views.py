from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EduVideoLecture
from .serializer import EduVideoLectureSerializer, EduVideoLecturesSerializer


class EduVideoLectureView(APIView):

    def get(self, request):
        lecture = EduVideoLecture.objects.all()
        serializer = EduVideoLecturesSerializer(lecture, many=True).data
        return Response(serializer)

    def post(self, request):
        if False: #관리자 로직 추가 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if True:#validation 추가
            # videolecture= EduVideoLecture.objects.create(
            #     writer_id=request.user.id,
            #     videoURL=request.data["videoURL"],
            #     videoExplanation=request.data["videoExplanation"],
            #     title=request.data["title"],
            #     isCharged=request.data["isCharged"],
            # )

            serializer = EduVideoLectureSerializer(data=request.data)
            if serializer.is_valid():#validation 로직 손보기
                serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EduVideoLectureViewWithPk(APIView):

    def get_videoLecture(self, pk):
        try:
            videoLecture = EduVideoLecture.objects.get(pk=pk)
            return videoLecture
        except videoLecture.DoesNotExist:
            return None

    def get(self, request, pk):
        videoLecture = self.get_videoLecture(pk)
        if videoLecture ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True: #로그인 로직 추가 필요
            serializer = EduVideoLectureSerializer(videoLecture).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    # update
    def put(self, request, pk):
        videoLecture = self.get_videoLecture(pk)
        if videoLecture == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False: #관리자 권한
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = EduVideoLectureSerializer(videoLecture, data=request.data, partial=True)
        if serializer.is_valid():#validate 로직 추가
            videoLecture = serializer.save()
            return Response(EduVideoLectureSerializer(videoLecture).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        videolecture = self.get_videoLecture(pk)
        if False: #videolecture.user != request.user: #관리자 로직 로그인 추가 필요
            return Response(status=status.HTTP_403_FORBIDDEN)
        if True:#관리자 로직
            videolecture.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)