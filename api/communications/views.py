from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from config.customExceptions import get_object_or_404_custom, get_object_or_404_custom_isTemporary
from config.customPermissions import IsGetRequestOrAuthenticated, IsGetRequestOrWriterOrAdminUser
from config.utils import HitCountResponse, ddAnonymousUser, DDCustomListAPiView
from .models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, VelogComment
from .serializer import ContestDebatesSerializer, ContestDebateSerializer, ContestCodeNotesSerializer, \
    ContestCodeNoteSerializer, VelogSerializer, VelogsSerializer, DebateCommentSerializer, CodeNoteCommentSerializer, \
    VelogCommentSerializer, ContestDebateSerializerForPost, \
    DebateCommentSerializerForPost, CodeNoteCommentSerializerForPost, VelogCommentSerializerForPost, \
    VelogSerializerForPost

from ..contests.models import Contest
from rest_framework.filters import SearchFilter, OrderingFilter


class ContestDebateListView(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = ContestDebate.dd_objects.all().order_by('-id')
    serializer_class = ContestDebatesSerializer
    # pagination_class 안 써주면 settings.py 에 있는 default 설정 따라감.
    # pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    # ListAPIView 에 list 기본 함수가 있지만, serializer 에 context 를 넣어주기 위해서 overriding 을 함.
    def list(self, request, *args, **kwargs):
        # 반드시 여기다가 filter_queryset 함수를 달아야 함.
        # paginate_queryset 하면 그 결과는 list object 가 돼서 filtering 하면 에러가 난다.
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestDebatesSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = ContestDebatesSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class ContestDebateListViewWithContestPK(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = ContestDebate.dd_objects.all().order_by('-id')
    serializer_class = ContestDebatesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    def list(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset().filter(contest_id=pk))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestDebatesSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = ContestDebatesSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestDebateCreateWithContestPk(request, pk):
    contest = get_object_or_404_custom(Contest, pk=pk)

    serializer = ContestDebateSerializerForPost(data=request.data)
    if serializer.is_valid():
        contestDebate = serializer.save(writer=request.user, contest=contest)
        returnSerializer = ContestDebateSerializer(contestDebate, context={'user': request.user})
        return Response(returnSerializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestDebateViewWithPk(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_contestDebate(self, pk):
        contestDebate = get_object_or_404_custom_isTemporary(ContestDebate, pk=pk)
        self.check_object_permissions(self.request, contestDebate)
        return contestDebate

    def get(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        serializer = ContestDebateSerializer(contestDebate, context={'user': request.user})
        return HitCountResponse(request, contestDebate, Response(serializer.data))

    def put(self, request, pk):
        contestDebate = self.get_contestDebate(pk)

        serializer = ContestDebateSerializer(contestDebate, data=request.data, partial=True,
                                             context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        contestDebate.delete()
        return Response(status=status.HTTP_200_OK)


class ContestCodeNoteListView(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = ContestCodeNote.dd_objects.all().order_by('-id')
    serializer_class = ContestCodeNotesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestCodeNotesSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = ContestCodeNotesSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class ContestCodeNoteListViewWithContestPK(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = ContestCodeNote.dd_objects.all().order_by('-id')
    serializer_class = ContestCodeNotesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    def list(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset().filter(contest_id=pk))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContestCodeNotesSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = ContestCodeNotesSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestCodeNoteCreateWithContestPk(request, pk):
    contest = get_object_or_404_custom(Contest, pk=pk)
    serializer = ContestCodeNoteSerializer(data=request.data)
    if serializer.is_valid():
        contestCodeNote = serializer.save(writer=request.user, contest=contest)
        returnSerializer = ContestCodeNoteSerializer(contestCodeNote, context={'user': request.user})
        return Response(returnSerializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestCodeNoteViewWithPk(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_contestCodeNote(self, pk):
        contestCodeNote = get_object_or_404_custom_isTemporary(ContestCodeNote, pk=pk)
        self.check_object_permissions(self.request, contestCodeNote)
        return contestCodeNote

    def get(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        serializer = ContestCodeNoteSerializer(contestCodeNote, context={'user': request.user})
        return HitCountResponse(request, contestCodeNote, Response(serializer.data))

    def put(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)

        serializer = ContestCodeNoteSerializer(contestCodeNote, data=request.data, partial=True,
                                               context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        contestCodeNote.delete()
        return Response(status=status.HTTP_200_OK)


class VelogListView(DDCustomListAPiView):
    permission_classes = [IsGetRequestOrAuthenticated]
    queryset = Velog.dd_objects.all().order_by('-id')
    serializer_class = VelogsSerializer
    # pagination_class 안 써주면 settings.py 에 있는 default 설정 따라감.
    # pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'writer__customProfile__nickname')
    ordering_fields = ('hitNums', 'id')

    # ListAPIView 에 list 기본 함수가 있지만, serializer 에 context 를 넣어주기 위해서 overriding 을 함.
    def list(self, request, *args, **kwargs):
        # 반드시 여기다가 filter_queryset 함수를 달아야 함.
        # paginate_queryset 하면 그 결과는 list object 가 돼서 filtering 하면 에러가 난다.
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = VelogsSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)
        serializer = VelogsSerializer(queryset, many=True, context={'user': request.user})
        return Response(serializer.data)


class VelogView(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def post(self, request):
        serializer = VelogSerializerForPost(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            velog = serializer.save(writer=request.user)
            returnSerializer = VelogSerializer(velog, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VelogViewWithPk(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_velog(self, pk):
        velog = get_object_or_404_custom_isTemporary(Velog, pk=pk)
        self.check_object_permissions(self.request, velog)
        return velog

    def get(self, request, pk):
        velog = self.get_velog(pk)
        serializer = VelogSerializer(velog, context={'user': request.user})
        return HitCountResponse(request, velog, Response(serializer.data))

    def put(self, request, pk):
        velog = self.get_velog(pk)
        serializer = VelogSerializer(velog, data=request.data, partial=True, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        velog = self.get_velog(pk)
        velog.delete()
        return Response(status=status.HTTP_200_OK)


# Debate pk에 따라 달린 댓글들을 보낼예정 대댓글은 안보냄, 댓글생성시이용
class DebateCommentViewWithDebatePK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        debateComment = DebateComment.objects.filter(contestDebate_id=pk)
        serializer = DebateCommentSerializer(debateComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        # 프론트엔드에서 안 담아주면 none 으로 처리됨.
        parent_debateComment_id = request.data.get('debateComment_id')
        parent_debateComment = None
        if parent_debateComment_id:
            parent_debateComment = get_object_or_404_custom(DebateComment, pk=parent_debateComment_id)
        contestDebate = get_object_or_404_custom(ContestDebate, pk=pk)
        serializer = DebateCommentSerializerForPost(data=request.data)
        if serializer.is_valid():
            debateComment = serializer.save(writer=request.user, contestDebate=contestDebate,
                                            debateComment=parent_debateComment)
            returnSerializer = DebateCommentSerializer(debateComment, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebateCommentViewWithPK(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]  # 댓글 수정 삭제. get 요청은 잘 안 쓸 것 같긴한데 나중에 혹시 ajax 에서 쓸 수 있으니 구현함.

    def get_debateComment(self, pk):
        debateComment = get_object_or_404_custom(DebateComment, pk=pk)
        self.check_object_permissions(self.request, debateComment)
        return debateComment

    def get(self, request, pk):
        debateComment = self.get_debateComment(pk)
        serializer = DebateCommentSerializer(debateComment, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        debateComment = self.get_debateComment(pk)

        serializer = DebateCommentSerializer(debateComment, data=request.data, partial=True,
                                             context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if DebateComment.objects.filter(debateComment=debateComment) or debateComment.debateComment:
            debateComment.writer = ddAnonymousUser
            debateComment.content = '삭제된 댓글입니다.'
            debateComment.save()

        else:
            debateComment.delete()

        return Response(status=status.HTTP_200_OK)


class CodeNoteCommentViewWithCodeNotePK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        codeNoteComment = CodeNoteComment.objects.filter(contestCodeNote_id=pk)
        serializer = CodeNoteCommentSerializer(codeNoteComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        # 프론트엔드에서 안 담아주면 none 으로 처리됨.
        parent_codeNoteComment_id = request.data.get('codeNoteComment_id')
        parent_codeNoteComment = None
        if parent_codeNoteComment_id:
            parent_codeNoteComment = get_object_or_404_custom(CodeNoteComment, pk=parent_codeNoteComment_id)
        contestCodeNote = get_object_or_404_custom(ContestCodeNote, pk=pk)
        serializer = CodeNoteCommentSerializerForPost(data=request.data)
        if serializer.is_valid():
            codeNoteComment = serializer.save(writer=request.user, contestCodeNote=contestCodeNote,
                                              codeNoteComment=parent_codeNoteComment)
            returnSerializer = CodeNoteCommentSerializer(codeNoteComment, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeNoteCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_codeNoteComment(self, pk):
        codeNoteComment = get_object_or_404_custom(CodeNoteComment, pk=pk)
        self.check_object_permissions(self.request, codeNoteComment)
        return codeNoteComment

    def get(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        serializer = CodeNoteCommentSerializer(codeNoteComment, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)

        serializer = CodeNoteCommentSerializer(codeNoteComment, data=request.data, partial=True,
                                               context={"user": request.user})
        if serializer.is_valid():  # validate 로직 추가
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if CodeNoteComment.objects.filter(codeNoteComment=codeNoteComment) or codeNoteComment.codeNoteComment:
            codeNoteComment.writer = ddAnonymousUser
            codeNoteComment.content = '삭제된 댓글입니다.'
            codeNoteComment.save()

        else:
            codeNoteComment.delete()

        return Response(status=status.HTTP_200_OK)


class VelogCommentViewWithVelogPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        velogComment = VelogComment.objects.filter(velog_id=pk)
        serializer = VelogCommentSerializer(velogComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        # 프론트엔드에서 안 담아주면 none 으로 처리됨.
        parent_velogComment_id = request.data.get('velogComment_id')
        parent_velogComment = None
        if parent_velogComment_id:
            parent_velogComment = get_object_or_404_custom(VelogComment, pk=parent_velogComment_id)
        velog = get_object_or_404_custom(Velog, pk=pk)
        serializer = VelogCommentSerializerForPost(data=request.data)
        if serializer.is_valid():
            velogComment = serializer.save(writer=request.user, velog=velog, velogComment=parent_velogComment)
            returnSerializer = VelogCommentSerializer(velogComment, context={"user": request.user})
            return Response(returnSerializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VelogCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_velogComment(self, pk):
        velogComment = VelogComment.objects.get(pk=pk)
        self.check_object_permissions(self.request, velogComment)
        return velogComment

    def get(self, request, pk):
        velogComment = self.get_velogComment(pk)
        serializer = VelogCommentSerializer(velogComment, context={'user': request.user})
        return Response(serializer.data)

    def put(self, request, pk):
        velogComment = self.get_velogComment(pk)

        serializer = VelogCommentSerializer(velogComment, data=request.data, partial=True,
                                            context={"user": request.user})
        if serializer.is_valid():  # validate 로직 추가
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if VelogComment.objects.filter(velogComment=velogComment) or velogComment.velogComment:
            velogComment.writer = ddAnonymousUser
            velogComment.content = '삭제된 댓글입니다.'
            velogComment.save()

        else:
            velogComment.delete()

        return Response(status=status.HTTP_200_OK)


# like 를 안 한 상태에서 like 를 하거나, 스크랩을 안 한 상태에서 scrap 을 하면 202_ACCEPTED
# status 를 줘서 프론트엔드 단에서 구별할 수 있게 해 주었다.

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestDebateLike(request, pk):
    contestDebate = get_object_or_404_custom(ContestDebate, pk=pk)
    if contestDebate.likes.filter(id=request.user.id).exists():
        contestDebate.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        contestDebate.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestCodeNoteLike(request, pk):
    contestCodenote = get_object_or_404_custom(ContestCodeNote, pk=pk)
    if contestCodenote.likes.filter(id=request.user.id).exists():
        contestCodenote.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        contestCodenote.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def VelogLike(request, pk):
    velog = get_object_or_404_custom(Velog, pk=pk)
    if velog.likes.filter(id=request.user.id).exists():
        velog.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        velog.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestDebateScrap(request, pk):
    contestDebate = get_object_or_404_custom(ContestDebate, pk=pk)
    if contestDebate.scrapProfiles.filter(id=request.user.customProfile.id).exists():
        request.user.customProfile.debateScraps.remove(contestDebate)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.debateScraps.add(contestDebate)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestCodenoteScrap(request, pk):
    contestCodenote = get_object_or_404_custom(ContestCodeNote, pk=pk)
    if contestCodenote.scrapProfiles.filter(id=request.user.customProfile.id).exists():
        request.user.customProfile.codeNoteScraps.remove(contestCodenote)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.codeNoteScraps.add(contestCodenote)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def VelogScrap(request, pk):
    velog = get_object_or_404_custom(Velog, pk=pk)
    if velog.scrapProfiles.filter(id=request.user.customProfile.id).exists():
        request.user.customProfile.velogScraps.remove(velog)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.velogScraps.add(velog)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def DebateCommentLike(request, pk):
    debateComment = get_object_or_404_custom(DebateComment, pk=pk)
    if debateComment.likes.filter(id=request.user.id).exists():
        debateComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        debateComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def CodeNoteCommentLike(request, pk):
    codeNoteComment = get_object_or_404_custom(CodeNoteComment, pk=pk)
    if codeNoteComment.likes.filter(id=request.user.id).exists():
        codeNoteComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        codeNoteComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def VelogCommentLike(request, pk):
    velogComment = get_object_or_404_custom(VelogComment, pk=pk)
    if velogComment.likes.filter(id=request.user.id).exists():
        velogComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        velogComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def temporaryContestDebate(request):
    contestDebates=ContestDebate.objects.filter(wirter=request.user, isTemporary=True)
    serializer = ContestDebatesSerializer(contestDebates,many=True, context={'user': request.user})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def temporaryContestCodeNote(request):
    contestCodeNotes=ContestCodeNote.objects.filter(wirter=request.user, isTemporary=True)
    serializer = ContestCodeNotesSerializer(contestCodeNotes, many=True, context={'user': request.user})
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def temporaryVelog(request):
    velog=Velog.objects.filter(wirter=request.user, isTemporary=True)
    serializer = VelogsSerializer(velog, many=True, context={'user': request.user})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
