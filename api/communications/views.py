from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContestDebate, ContestCodeNote, Velog, DebateComment, CodeNoteComment, VelogComment
from .serializers import ContestDebatesSerializer, ContestDebateSerializer, ContestCodeNotesSerializer, \
    ContestCodeNoteSerializer, VelogSerializer, VelogsSerializer, DebateCommentSerializer, CodeNoteCommentSerializer, \
    VelogCommentSerializer


# post, put validation 에서 hitnum, likes, writer 등등 추가적으로 추가/수정해야 함.
# serialize.save 안 쓰는 것도 고려해 볼 만한 대안임. read_only field 를 적극 활용하는 방법도 있음.

class ContestDebateView(APIView):
    permission_classes = [IsGetRequestOrAuthenticated]

    def get(self, request):
        contestDebate = ContestDebate.objects.all()
        serializer = ContestDebatesSerializer(contestDebate, many=True, context={'user': request.user})
        # context = {'request':request} 로 request 객체 받아서 쓸 수도 있음
        return Response(serializer.data)

    def post(self, request):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestDebateSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            # serializer.save(writer=request.user)  # 로그인 안하면 지금 오류남
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestDebateViewWithPk(APIView):

    def get_contestDebate(self, pk):
        try:
            contestDebate = ContestDebate.objects.get(pk=pk)
            return contestDebate
        except contestDebate.DoesNotExist:
            return None

    def get(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestDebateSerializer(contestDebate, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestDebateSerializer(contestDebate, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            contestDebate = serializer.save()
            return Response(ContestDebateSerializer(contestDebate).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == self.writer  or 관리자
            contestDebate.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ContestCodeNoteView(APIView):

    def get(self, request):
        contestCodeNote = ContestCodeNote.objects.all()
        serializer = ContestCodeNotesSerializer(contestCodeNote, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestCodeNoteSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestCodeNoteViewWithPk(APIView):

    def get_contestCodeNote(self, pk):
        try:
            contestCodeNote = ContestCodeNote.objects.get(pk=pk)
            return contestCodeNote
        except contestCodeNote.DoesNotExist:
            return None

    def get(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestCodeNoteSerializer(contestCodeNote, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestCodeNoteSerializer(contestCodeNote, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 검토
            contestCodeNote = serializer.save()
            return Response(ContestCodeNoteSerializer(contestCodeNote).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == self.writer  or 관리자
            contestCodeNote.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class VelogView(APIView):

    def get(self, request):
        velog = Velog.objects.all()
        serializer = VelogsSerializer(velog, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = VelogSerializer(data=request.data)
        if serializer.is_valid():  # validation 로직 손보기
            serializer.save(writer=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VelogViewWithPk(APIView):

    def get_velog(self, pk):
        try:
            velog = Velog.objects.get(pk=pk)
            return velog
        except velog.DoesNotExist:
            return None

    def get(self, request, pk):
        velog = self.get_velog(pk)
        if velog == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VelogSerializer(velog, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        velog = self.get_velog(pk)
        if velog == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = VelogSerializer(velog, data=request.data, partial=True)
        if serializer.is_valid():  # validate 로직 추가
            velog = serializer.save()
            return Response(VelogSerializer(velog).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        velog = self.get_velog(pk)
        if velog == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == self.writer  or 관리자
            velog.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# Debate pk에 따라 달린 댓글들을 보낼예정 대댓글은 안보냄, 댓글생성시이용
class DebateCommentViewWithDebatePK(APIView):

    def get(self, request, pk):
        debateComment = DebateComment.objects.filter(contestDebate_id=pk)
        serializer = DebateCommentSerializer(debateComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # serializer 를 안 쓰고 그냥 처리함.
        debateComment = DebateComment.objects.create(
            writer=request.user,
            content=request.data["content"],
            contestDebate_id=pk,
            debateComment_id=request.data["debateComment"]
        )
        serializer = DebateCommentSerializer(debateComment)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DebateCommentViewWithPK(APIView):  # 댓글 수정 삭제. get 요청은 잘 안 쓸 것 같긴한데 나중에 혹시 ajax 에서 쓸 수 있으니 구현함.

    def get_debateComment(self, pk):
        try:
            debateComment = DebateComment.objects.get(pk=pk)
            return debateComment
        except debateComment.DoesNotExist:
            return None

    def get(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if debateComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = DebateCommentSerializer(debateComment, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if debateComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = DebateCommentSerializer(debateComment, data=request.data, partial=True, )
        if serializer.is_valid():  # validate 로직 추가
            debateComment = serializer.save()
            return Response(DebateCommentSerializer(debateComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        debateComment = self.get_debateComment(pk)
        if debateComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == self.writer  or 관리자
            debateComment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CodeNoteCommentViewWithCodeNotePK(APIView):

    def get(self, request, pk):
        codeNoteComment = CodeNoteComment.objects.filter(contestCodeNote_id=pk)
        serializer = CodeNoteCommentSerializer(codeNoteComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        codeNoteComment = CodeNoteComment.objects.create(
            writer=request.user,
            content=request.data["content"],
            contestCodeNote_id=pk,
            codeNoteComment_id=request.data["debateComment"]
        )
        serializer = DebateCommentSerializer(codeNoteComment)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CodeNoteCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈

    def get_codeNoteComment(self, pk):
        try:
            codeNoteComment = CodeNoteComment.objects.get(pk=pk)
            return codeNoteComment
        except codeNoteComment.DoesNotExist:
            return None

    def get(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if codeNoteComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CodeNoteCommentSerializer(codeNoteComment, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if codeNoteComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = CodeNoteCommentSerializer(codeNoteComment, data=request.data, partial=True, )
        if serializer.is_valid():  # validate 로직 추가
            codeNoteComment = serializer.save()
            return Response(CodeNoteCommentSerializer(codeNoteComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        codeNoteComment = self.get_codeNoteComment(pk)
        if codeNoteComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == self.writer  or 관리자
            codeNoteComment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class VelogCommentViewWithVelogPK(APIView):

    def get(self, request, pk):
        velogComment = VelogComment.objects.filter(Velog_id=pk)
        serializer = VelogCommentSerializer(velogComment, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request, pk):
        if False:  # 로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        velogComment = VelogComment.objects.create(
            writer=request.user,
            content=request.data["content"],
            velog_id=pk,
            velogComment_id=request.data["velogComment"]
        )
        serializer = VelogCommentSerializer(velogComment)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class VelogCommentViewWithPK(APIView):  # 댓글 수정삭제, get요청은 잘안쓸거같긴한데 나중에 혹시 ajax에서 쓸수있으니 구현해놈

    def get_velogComment(self, pk):
        try:
            velogComment = VelogComment.objects.get(pk=pk)
            return velogComment
        except velogComment.DoesNotExist:
            return None

    def get(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if velogComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VelogCommentSerializer(velogComment, context={'user': request.user})
            return Response(serializer.data)

    def put(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if velogComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False:  # request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = VelogCommentSerializer(velogComment, data=request.data, partial=True, )
        if serializer.is_valid():  # validate 로직 추가
            velogComment = serializer.save()
            return Response(VelogCommentSerializer(velogComment).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        velogComment = self.get_velogComment(pk)
        if velogComment == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:  # request.user == self.writer  or 관리자
            velogComment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
