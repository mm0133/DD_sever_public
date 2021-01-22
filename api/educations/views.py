from rest_framework import status, permissions, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from config.customPermissions import IsGetRequestOrAdminUser, IsGetRequestOrAuthenticated, \
    IsGetRequestOrWriterOrAdminUser
from config.customExceptions import get_object_or_404_custom
from config.utils import HitCountResponse, ddAnonymousUser, DDCustomListAPiView
from .models import EduVideoLecture, LecturePackage, LecturePackageComment, EduVideoLectureComment, LectureNoteComment
from .serializer import EduVideoLectureSerializer, EduVideoLecturesSerializer, LecturePackageSerializer, \
    LecturePackageSerializerForPost, LecturePackageCommentSerializer, EduVideoLectureCommentSerializer, \
    LecturePackageCommentSerializerForPostPUT, EduVideoLectureCommentSerializerForPostPut, LectureNoteCommentSerializer, \
    LectureNoteCommentSerializerForPost


class LecturePackageListView(DDCustomListAPiView):
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
            lecturePackage = serializer.save(writer=request.user)
            return Response(data=LecturePackageSerializer(lecturePackage).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LecturePackageViewWithPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        serializer = LecturePackageSerializer(lecturePackage, context={"user": request.user})
        return HitCountResponse(request, lecturePackage, Response(serializer.data))

    def put(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
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
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        videoLectures = EduVideoLecture.objects.filter(lecturePackage=lecturePackage)
        serializer = EduVideoLecturesSerializer(videoLectures, many=True, context={"user": request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        serializer = EduVideoLectureSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save(writer=request.user, lecturePackage_id=pk)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EduVideoLectureViewWithVideoPk(APIView):
    permission_classes = [IsGetRequestOrAdminUser]

    def get(self, request, pk):
        videoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
        serializer = EduVideoLectureSerializer(videoLecture, context={"user": request.user})
        return HitCountResponse(request, videoLecture, Response(serializer.data))

    def put(self, request, pk):
        videoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
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
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        lecturePackageComments = LecturePackageComment.objects.filter(lecturePackage=lecturePackage)
        serializer = LecturePackageCommentSerializer(lecturePackageComments, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        lecturePackage = get_object_or_404_custom(LecturePackage, pk=pk)
        serializer = LecturePackageCommentSerializerForPostPUT(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            comment = serializer.save(writer=request.user, lecturePackage=lecturePackage)
            return Response(LecturePackageCommentSerializer(comment).data)
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
        lecturePackageComment.writer = ddAnonymousUser
        lecturePackageComment.content = ''
        lecturePackageComment.save()
        return Response(status=status.HTTP_200_OK)


class EduVideoLectureCommentsViewWithVideoPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        eduVideoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
        eduVideoLectureComments = EduVideoLectureComment.objects.filter(eduVideoLecture=eduVideoLecture)
        serializer = EduVideoLectureCommentSerializer(eduVideoLectureComments, many=True,
                                                      context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        eduVideoLecture = get_object_or_404_custom(EduVideoLecture, pk=pk)
        serializer = EduVideoLectureCommentSerializerForPostPut(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            eduVideoLectureComment = serializer.save(writer=request.user, eduVideoLecture=eduVideoLecture)
            return Response(EduVideoLectureCommentSerializer(eduVideoLectureComment).data)
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
        eduVideoLectureComment.writer = ddAnonymousUser
        eduVideoLectureComment.content = ''
        eduVideoLectureComment.save()
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








class LectureNoteCommentViewWithPage(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, page):
        lectureNoteComment = LectureNoteComment.objects.filter(page=page)
        serializer = LectureNoteCommentSerializer(lectureNoteComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, page):
        # 프론트엔드에서 안 담아주면 none 으로 처리됨.
        parent_Comment_id = request.data.get('lectureNoteComment_id')
        parent_Comment = None
        if parent_Comment_id:
            parent_Comment = get_object_or_404_custom(LectureNoteComment, pk=parent_Comment_id)



        serializer = LectureNoteCommentSerializerForPost(data=request.data)
        if serializer.is_valid():
            lectureNoteComment = serializer.save(writer=request.user, lectureNoteComment=parent_Comment,
                                              page=page)
            returnSerializer = LectureNoteCommentSerializer(lectureNoteComment, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class LectureNoteCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_lectureNoteComment(self, pk):
        lectureNoteComment = get_object_or_404_custom(LectureNoteComment, pk=pk)
        self.check_object_permissions(self.request, lectureNoteComment)
        return lectureNoteComment

    def get(self, request, pk):
        lectureNoteComment = self.get_lectureNoteComment(pk)
        serializer = LectureNoteCommentSerializer(lectureNoteComment, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        lectureNoteComment = self.get_lectureNoteComment(pk)

        serializer = LectureNoteCommentSerializer(lectureNoteComment, data=request.data, partial=True,
                                               context={"user": request.user})
        if serializer.is_valid():  # validate 로직 추가
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lectureNoteComment = self.get_lectureNoteComment(pk)
        if LectureNoteComment.objects.filter(lectureNoteComment=lectureNoteComment) or lectureNoteComment.lectureNoteComment:
            lectureNoteComment.writer = ddAnonymousUser
            lectureNoteComment.content = '삭제된 댓글입니다.'
            lectureNoteComment.save()

        else:
            lectureNoteComment.delete()

        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def LectureNoteCommentLike(request, pk):
    lectureNoteComment = get_object_or_404_custom(LectureNoteComment, pk=pk)
    if lectureNoteComment.likes.filter(id=request.user.id).exists():
        lectureNoteComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        lectureNoteComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)