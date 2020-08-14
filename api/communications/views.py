from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from config.customPermissions import IsGetRequestOrAuthenticated, IsGetRequestOrWriterOrAdminUser
from config.utils import hitCountRespose
from .models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, VelogComment
from .serializers import ContestDebatesSerializer, ContestDebateSerializer, ContestCodeNotesSerializer, \
    ContestCodeNoteSerializer, VelogSerializer, VelogsSerializer, DebateCommentSerializer, CodeNoteCommentSerializer, \
    VelogCommentSerializer

# post, put validation 에서 hitnum, likes, writer 등등 추가적으로 추가/수정해야 함.
# serialize.save 안 쓰는 것도 고려해 볼 만한 대안임. read_only field 를 적극 활용하는 방법도 있음.
from ..contests.models import Contest


class ContestDebateView(APIView):
    def get(self, request):
        contestDebate = ContestDebate.objects.all()
        serializer = ContestDebatesSerializer(contestDebate, many=True, context={'user': request.user})
        # context = {'request':request} 로 request 객체 받아서 쓸 수도 있음
        return Response(serializer.data)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestDebateCreateWithContestPk(request, pk):
    contest = get_object_or_404(Contest, pk=pk)
    contestDebate = ContestDebate.objects.create(
        writer=request.user,
        content=request.data["content"],
        title=request.data["title"],
        contest=contest
    )

    serializer = ContestDebatesSerializer(contestDebate, context={"user":request.user})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ContestDebateViewWithPk(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_contestDebate(self, pk):
        try:
            contestDebate = get_object_or_404(ContestDebate, pk=pk)
            self.check_object_permissions(self.request, contestDebate)
            return contestDebate
        except contestDebate.DoesNotExist:
            return None

    def get(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestDebateSerializer(contestDebate, context={'user': request.user})
            return hitCountRespose(request, contestDebate, Response(serializer.data))

    def put(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ContestDebateSerializer(contestDebate, data=request.data, partial=True, context={"user":request.user})
        if serializer.is_valid():  # validate 로직 추가
            contestDebate = serializer.save()
            return Response(ContestDebateSerializer(contestDebate).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contestDebate.delete()
        return Response(status=status.HTTP_200_OK)


class ContestCodeNoteView(APIView):

    def get(self, request):
        contestCodeNote = ContestCodeNote.objects.all()
        serializer = ContestCodeNotesSerializer(contestCodeNote, many=True, context={'user': request.user})
        return Response(serializer.data)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestCodenoteCreateWithContestPk(request, pk):
    contest = get_object_or_404(Contest, pk=pk)
    contestCodenote = ContestCodeNote.objects.create(
        writer=request.user,
        content=request.data["content"],
        title=request.data["title"],
        contest=contest
    )

    serializer = CodeNoteCommentSerializer(contestCodenote,  context={"user":request.user})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ContestCodeNoteViewWithPk(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_contestCodeNote(self, pk):
        try:
            contestCodeNote = ContestCodeNote.objects.get(pk=pk)
            self.check_object_permissions(self.request, contestCodeNote)
            return contestCodeNote
        except contestCodeNote.DoesNotExist:
            return None

    def get(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestCodeNoteSerializer(contestCodeNote, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ContestCodeNoteSerializer(contestCodeNote, data=request.data, partial=True, context={"user":request.user})
        if serializer.is_valid():  # validate 로직 검토
            contestCodeNote = serializer.save()
            return Response(ContestCodeNoteSerializer(contestCodeNote).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contestCodeNote.delete()
        return Response(status=status.HTTP_200_OK)


class VelogView(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request):
        velog = Velog.objects.all()
        serializer = VelogsSerializer(velog, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request):
        serializer = VelogSerializer(data=request.data, context={"user":request.user})
        if serializer.is_valid():  # validation 로직 손보기
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VelogViewWithPk(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_velog(self, pk):
        try:
            velog = Velog.objects.get(pk=pk)
            self.check_object_permissions(self.request, velog)
            return velog
        except velog.DoesNotExist:
            return None

    def get(self, request, pk):
        velog = self.get_velog(pk)
        if velog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VelogSerializer(velog, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        velog = self.get_velog(pk)
        if velog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VelogSerializer(velog, data=request.data, partial=True, context={"user":request.user})
        if serializer.is_valid():  # validate 로직 추가
            velog = serializer.save()
            return Response(VelogSerializer(velog).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        velog = self.get_velog(pk)
        if velog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
        # serializer 를 안 쓰고 그냥 처리함.
        # parent_debateComment를 프론트엔드에서 주지 않으면 대댓이 아니라 그냥 댓글이라고 판단 가능.
        # 에러가 안 나려면 밑과 같이 처리해줘야 한다.
        if 'debateComment' in request.data:
            parent_debateComment_id = request.data['debateComment']
            # 다른 debate에 달려 있는 debateComment에 대댓을 달지 못하게 하는 코드
            parent_debateComment = get_object_or_404(DebateComment, pk=parent_debateComment_id)
            if parent_debateComment.contestDebate.id is not pk:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            parent_debateComment_id = None
        debateComment = DebateComment.objects.create(
            writer=request.user,
            content=request.data["content"],
            contestDebate_id=pk,
            debateComment_id=parent_debateComment_id
        )
        serializer = DebateCommentSerializer(debateComment, context={"user":request.user})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DebateCommentViewWithPK(APIView):
    permission_classes = [IsGetRequestOrWriterOrAdminUser]  # 댓글 수정 삭제. get 요청은 잘 안 쓸 것 같긴한데 나중에 혹시 ajax 에서 쓸 수 있으니 구현함.

    def get_debateComment(self, pk):
        try:
            debateComment = DebateComment.objects.get(pk=pk)
            self.check_object_permissions(self.request, debateComment)
            return debateComment
        except debateComment.DoesNotExist:
            return None

    def get(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if debateComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = DebateCommentSerializer(debateComment, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if debateComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DebateCommentSerializer(debateComment, data=request.data, partial=True, context={"user":request.user})
        if serializer.is_valid():  # validate 로직 추가
            debateComment = serializer.save()
            return Response(DebateCommentSerializer(debateComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if debateComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        debateComment.delete()
        return Response(status=status.HTTP_200_OK)


class CodeNoteCommentViewWithCodeNotePK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        codeNoteComment = CodeNoteComment.objects.filter(contestCodeNote_id=pk)
        serializer = CodeNoteCommentSerializer(codeNoteComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        if 'codenoteComment' in request.data:
            parent_codenoteComment_id = request.data['codenoteComment']
            # 다른 debate에 달려 있는 codenoteComment에 대댓을 달지 못하게 하는 코드
            parent_codenoteComment = get_object_or_404(CodeNoteComment, pk=parent_codenoteComment_id)
            if parent_codenoteComment.codenoteComment.id is not pk:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            parent_codenoteComment_id = None

        codeNoteComment = CodeNoteComment.objects.create(
            writer=request.user,
            content=request.data["content"],
            contestCodeNote_id=pk,
            codeNoteComment_id=parent_codenoteComment_id
        )
        serializer = CodeNoteCommentSerializer(codeNoteComment,context={"user":request.user})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CodeNoteCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_codeNoteComment(self, pk):
        try:
            codeNoteComment = CodeNoteComment.objects.get(pk=pk)
            self.check_object_permissions(self.request, codeNoteComment)
            return codeNoteComment
        except codeNoteComment.DoesNotExist:
            return None

    def get(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if codeNoteComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CodeNoteCommentSerializer(codeNoteComment, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if codeNoteComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CodeNoteCommentSerializer(codeNoteComment, data=request.data, partial=True, context={"user":request.user})
        if serializer.is_valid():  # validate 로직 추가
            codeNoteComment = serializer.save()
            return Response(CodeNoteCommentSerializer(codeNoteComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if codeNoteComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        codeNoteComment.delete()
        return Response(status=status.HTTP_200_OK)


class VelogCommentViewWithVelogPK(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request, pk):
        velogComment = VelogComment.objects.filter(velog_id=pk)
        serializer = VelogCommentSerializer(velogComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        if 'velogComment' in request.data:
            parent_velogComment_id = request.data['velogComment']
            # 다른 debate에 달려 있는 velogComment에 대댓을 달지 못하게 하는 코드
            parent_velogComment = get_object_or_404(VelogComment, pk=parent_velogComment_id)
            if parent_velogComment.velogComment.id is not pk:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            parent_velogComment_id = None
        velogComment = VelogComment.objects.create(
            writer=request.user,
            content=request.data["content"],
            velog_id=pk,
            # VelogComment에 VelogComment가 대문자로 시작해서 이렇게 적음
            # 나중에 모델 수정할 때 같이 고쳐야 함.
            # 다민
            velogComment_id=parent_velogComment_id
        )
        serializer = VelogCommentSerializer(velogComment, context={"user":request.user})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class VelogCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈
    permission_classes = [IsGetRequestOrWriterOrAdminUser]

    def get_velogComment(self, pk):
        try:
            velogComment = VelogComment.objects.get(pk=pk)
            self.check_object_permissions(self.request, velogComment)
            return velogComment
        except velogComment.DoesNotExist:
            return None

    def get(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if velogComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VelogCommentSerializer(velogComment, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if velogComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VelogCommentSerializer(velogComment, data=request.data, partial=True, context={"user":request.user})
        if serializer.is_valid():  # validate 로직 추가
            velogComment = serializer.save()
            return Response(VelogCommentSerializer(velogComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if velogComment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        velogComment.delete()
        return Response(status=status.HTTP_200_OK)


# like 를 안 한 상태에서 like 를 하거나, 스크랩을 안 한 상태에서 scrap 을 하면 202_ACCEPTED
# status 를 줘서 프론트엔드 단에서 구별할 수 있게 해 주었다.

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestDebateLike(request, pk):
    contestDebate = get_object_or_404(ContestDebate, pk=pk)
    if contestDebate.likes.filter(id=request.user.id).exists():
        contestDebate.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        contestDebate.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestCodeNoteLike(request, pk):
    contestCodenote = get_object_or_404(ContestCodeNote, pk=pk)
    if contestCodenote.likes.filter(id=request.user.id).exists():
        contestCodenote.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        contestCodenote.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def VelogLike(request, pk):
    velog = get_object_or_404(Velog, pk=pk)
    if velog.likes.filter(id=request.user.id).exists():
        velog.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        velog.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestDebateScrap(request, pk):
    contestDebate = get_object_or_404(ContestDebate, pk=pk)
    if contestDebate.scrapProfiles.filter(id=request.user.customProfile.id).exists():
        request.user.customProfile.debateScraps.remove(contestDebate)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.debateScraps.add(contestDebate)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def ContestCodenoteScrap(request, pk):
    contestCodenote = get_object_or_404(ContestCodeNote, pk=pk)
    if contestCodenote.scrapProfiles.filter(id=request.user.customProfile.id).exists():
        request.user.customProfile.codeNoteScraps.remove(contestCodenote)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.codeNoteScraps.add(contestCodenote)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def VelogScrap(request, pk):
    velog = get_object_or_404(Velog, pk=pk)
    if velog.scrapProfiles.filter(id=request.user.customProfile.id).exists():
        request.user.customProfile.velogScraps.remove(velog)
        return Response(status=status.HTTP_200_OK)
    else:
        request.user.customProfile.velogScraps.add(velog)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def DebateCommentLike(request, pk):
    debateComment = get_object_or_404(DebateComment, pk=pk)
    if debateComment.likes.filter(id=request.user.id).exists():
        debateComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        debateComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def CodeNoteCommentLike(request, pk):
    codeNoteComment = get_object_or_404(CodeNoteComment, pk=pk)
    if codeNoteComment.likes.filter(id=request.user.id).exists():
        codeNoteComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        codeNoteComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def VelogCommentLike(request, pk):
    velogComment = get_object_or_404(VelogComment, pk=pk)
    if velogComment.likes.filter(id=request.user.id).exists():
        velogComment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    else:
        velogComment.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)
