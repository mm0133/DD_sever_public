from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.customPermissions import IsGetRequestOrAdminUser
from .models import EduVideoLecture, LecturePackage
from .serializer import EduVideoLectureSerializer, EduVideoLecturesSerializer, LecturePackageSerializer


class LecturePackageView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request):
        lecture = LecturePackage.objects.all()
        serializer = LecturePackageSerializer(lecture, many=True).data
        return Response(serializer)

    def post(self, request):
        serializer = LecturePackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LecturePackageViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get_lecturePackage(self, pk):
        try:
            lecturePackage = LecturePackage.objects.get(pk=pk)
            return lecturePackage
        except lecturePackage.DoesNotExist:
            return None

    def get(self, request, pk):

        lecturePackage = self.get_lecturePackage(pk)
        if lecturePackage is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LecturePackageSerializer(lecturePackage)
        return Response(serializer.data)

    def put(self, request, pk):
        lecturePackage = self.get_lecturePackage(pk)
        if lecturePackage is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LecturePackageSerializer(lecturePackage, data=request.data, partial=True)
        if serializer.is_valid():
            lecturePackage = serializer.save()
            return Response(LecturePackageSerializer(lecturePackage).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        videolecture = self.get_lecturePackage(pk)
        videolecture.delete()
        return Response(status=status.HTTP_200_OK)


class EduVideoLectureViewWithPackagePK(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        videoLectures = EduVideoLecture.objects.filter(lecturePackage_id=pk)
        serializer = EduVideoLecturesSerializer(videoLectures, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = EduVideoLectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user, lecturePackage_id=pk)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EduVideoLectureViewWithVideoPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get_videoLecture(self, pk):
        try:
            videoLecture = EduVideoLecture.objects.get(pk=pk)
            return videoLecture
        except videoLecture.DoesNotExist:
            return None

    def get(self, request, pk):
        videoLecture = self.get_videoLecture(pk)
        if videoLecture is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EduVideoLectureSerializer(videoLecture).data
        return Response(serializer)

    def put(self, request, pk):
        videoLecture = self.get_videoLecture(pk)
        if videoLecture is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EduVideoLectureSerializer(videoLecture, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            videoLecture = serializer.save()
            return Response(EduVideoLectureSerializer(videoLecture).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        videolecture = self.get_videoLecture(pk)
        videolecture.delete()
        return Response(status=status.HTTP_200_OK)
