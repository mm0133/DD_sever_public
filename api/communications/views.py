from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContestDebate, ContestCodeNote, Velog
from .serializers import ContestDebatesSerializer, ContestDebateSerializer, ContestCodeNotesSerializer, \
    ContestCodeNoteSerializer, VelogSerializer, VelogsSerializer


class ContestDebateView(APIView):

    def get(self, request):
        contestDebate =  ContestDebate.objects.all()
        serializer = ContestDebatesSerializer(contestDebate, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request):
        if False: #로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestDebateSerializer(data=request.data)
        if serializer.is_valid():#validation 로직 손보기
            serializer.save()
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
        if contestDebate ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestDebateSerializer(contestDebate,  context={'request': request})
            return Response(serializer.data)


    def put(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False: #request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestDebateSerializer(contestDebate, data=request.data, partial=True)
        if serializer.is_valid():#validate 로직 추가
            contestDebate = serializer.save()
            return Response(ContestDebateSerializer(contestDebate).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        contestDebate = self.get_contestDebate(pk)
        if contestDebate == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:# request.user == self.writer  or 관리자
            contestDebate.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class ContestCodeNoteView(APIView):

    def get(self, request):
        contestCodeNote = ContestCodeNote.objects.all()
        serializer = ContestCodeNotesSerializer(contestCodeNote, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if False: #로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestCodeNoteSerializer(data=request.data)
        if serializer.is_valid():#validation 로직 손보기
            serializer.save()
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
        if contestCodeNote ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContestCodeNoteSerializer(contestCodeNote, context={'request': request})
            return Response(serializer.data)


    def put(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False: #request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContestCodeNoteSerializer(contestCodeNote, data=request.data, partial=True)
        if serializer.is_valid():#validate 로직 검토
            contestCodeNote = serializer.save()
            return Response(ContestCodeNoteSerializer(contestCodeNote).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        contestCodeNote = self.get_contestCodeNote(pk)
        if contestCodeNote == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:# request.user == self.writer  or 관리자
            contestCodeNote.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class VelogView(APIView):

    def get(self, request):
        velog =  Velog.objects.all()
        serializer = VelogsSerializer(velog, many=True, context={'user': request.user})
        return Response(serializer.data)

    def post(self, request):
        if False: #로그인 인증 로직 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = VelogSerializer(data=request.data)
        if serializer.is_valid():#validation 로직 손보기
            serializer.save()
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
        if velog ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VelogSerializer(velog,  context={'request': request})
            return Response(serializer.data)


    def put(self, request, pk):
        velog = self.get_velog(pk)
        if velog == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if False: #request.user == self.writer  or 관리자
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = VelogSerializer(velog, data=request.data, partial=True)
        if serializer.is_valid():#validate 로직 추가
            velog = serializer.save()
            return Response(VelogSerializer(velog).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        velog = self.get_velog(pk)
        if velog == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if True:# request.user == self.writer  or 관리자
            velog.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class DebateCommentViewWithDebatePK(APIView)# Debate pk에 따라 달린 댓글들을 보낼예정 대댓글은 안보냄, 댓글생성시이용

class DebateCommentViewWithPK(APIView) #댓글 pk에 따라 수정 삭제 하게할 예정

class DebateReplyCommentViewWithCommentPK(APIView) #댓글 pk에 따른 대댓글을 전부보낼예정
