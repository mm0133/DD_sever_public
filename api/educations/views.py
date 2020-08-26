from rest_framework import status, permissions, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from config.customPermissions import IsGetRequestOrAdminUser, IsGetRequestOrAuthenticated, \
    IsGetRequestOrWriterOrAdminUser
from config.customExceptions import get_object_or_404_custom
from config.utils import HitCountResponse
from .models import EduVideoLecture, LecturePackage, LecturePackageComment, EduVideoLectureComment
from .serializer import EduVideoLectureSerializer, EduVideoLecturesSerializer, LecturePackageSerializer, \
    LecturePackageSerializerForPost, LecturePackageCommentSerializer, EduVideoLectureCommentSerializer, \
    LecturePackageCommentSerializerForPostPUT, EduVideoLectureCommentSerializerForPostPut


class LecturePackageListView(generics.ListAPIView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = LecturePackage.objects.all().order_by('-id')
    serializer_class = LecturePackageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LecturePackageSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = LecturePackageSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class LecturePackageCreateView(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def post(self, request):
        serializer = LecturePackageSerializerForPost(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LecturePackageViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        if lecturePackage is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LecturePackageSerializer(lecturePackage, context={"user": request.user})
        return HitCountResponse(request, lecturePackage, Response(serializer.data))

    def put(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        if lecturePackage is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LecturePackageSerializer(lecturePackage, data=request.data, partial=True,
                                              context={"user": request.user})
        if serializer.is_valid():
            lecturePackage = serializer.save()
            return Response(LecturePackageSerializer(lecturePackage).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        lecturePackage.delete()
        return Response(status=status.HTTP_200_OK)


class EduVideoLectureViewWithPackagePK(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        videoLectures = EduVideoLecture.objects.filter(lecturePackage_id=pk)
        serializer = EduVideoLecturesSerializer(videoLectures, many=True, context={"user": request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = EduVideoLectureSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save(writer=request.user, lecturePackage_id=pk)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EduVideoLectureViewWithVideoPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        videoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
        if videoLecture is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EduVideoLectureSerializer(videoLecture, context={"user": request.user})
        return HitCountResponse(request, videoLecture, Response(serializer.data))

    def put(self, request, pk):
        videoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
        if videoLecture is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EduVideoLectureSerializer(videoLecture, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            videoLecture = serializer.save()
            return Response(EduVideoLectureSerializer(videoLecture).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        videoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
        videoLecture.delete()
        return Response(status=status.HTTP_200_OK)


class LecturePackageCommentsViewWithPackagePK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        lecturePackageComments = LecturePackageComment.objects.filter(lecturePackage_id=pk)
        serializer = LecturePackageCommentSerializer(lecturePackageComments, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = LecturePackageCommentSerializerForPostPUT(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(writer=request.user, lecturePackage_id=pk)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LecturePackageCommentsViewWithPK(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_lecturePackageComment(self, pk):
        lecturePackageComment = get_object_or_404_custom(LecturePackageComment, pk=pk)
        self.check_object_permissions(self.request, lecturePackageComment)
        return lecturePackageComment

    def get(self, request, pk):
        lecturePackageComment = self.get_lecturePackageComment(pk)
        serializer = LecturePackageCommentSerializer(lecturePackageComment, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        lecturePackageComment = self.get_lecturePackageComment(pk)
        serializer = LecturePackageCommentSerializerForPostPUT(lecturePackageComment, data=request.data, partial=True,
                                                               context={'user': request.user})
        if serializer.is_valid():
            lecturePackageComment = serializer.save()
            return Response(LecturePackageCommentSerializer(lecturePackageComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lecturePackageComment = self.get_lecturePackageComment(pk)
        lecturePackageComment.delete()
        return Response(status=status.HTTP_200_OK)


class EduVideoLectureCommentsViewWithVideoPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        eduVideoLectureComments = EduVideoLectureComment.objects.filter(eduVideoLecture_id=pk)
        serializer = EduVideoLectureCommentSerializer(eduVideoLectureComments, many=True,
                                                      context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = EduVideoLectureCommentSerializerForPostPut(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(writer=request.user, eduVideoLecture_id=pk)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EduVideoLectureCommentViewWithPK(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_eduVideoLectureComment(self, pk):
        eduVideoLectureComment = get_object_or_404_custom(EduVideoLectureComment, pk=pk)
        self.check_object_permissions(self.request, eduVideoLectureComment)
        return eduVideoLectureComment

    def get(self, request, pk):
        eduVideoLectureComment = self.get_eduVideoLectureComment(pk)
        serializer = EduVideoLectureCommentSerializer(eduVideoLectureComment, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        eduVideoLectureComment = self.get_eduVideoLectureComment(pk)
        serializer = EduVideoLectureCommentSerializerForPostPut(eduVideoLectureComment, data=request.data, partial=True,
                                                                context={'user': request.user})
        if serializer.is_valid():
            eduVideoLectureComment = serializer.save()
            return Response(EduVideoLectureCommentSerializer(eduVideoLectureComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        eduVideoLectureComment = self.get_eduVideoLectureComment(pk)
        eduVideoLectureComment.delete()
        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def LecturePackageCommentLike(request, pk):
    lecturePackageComment = get_object_or_404_custom(LecturePackageComment, pk=pk)
    if lecturePackageComment.likes.filter(id=request.user.id).exists():
        lecturePackageComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        lecturePackageComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def EduVideoLectureCommentLike(request, pk):
    eduVideoLectureComment = get_object_or_404_custom(EduVideoLectureComment, pk=pk)
    if eduVideoLectureComment.likes.filter(id=request.user.id).exists():
        eduVideoLectureComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        eduVideoLectureComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)
