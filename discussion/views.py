from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from classroom.models import Class
from .models import Discussion, Response
from .serializers import DiscussionSerializer, ResponseSerializer, SolvedSerializer
from .permissions import IsStudentOrReadonly, IsTeacherOrStudent


# Create your views here.


class GetClassDiscussions(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsStudentOrReadonly)
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        return Discussion.objects.filter(classroom=self.kwargs['classpk']).select_related('created_by')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, classroom=Class.objects.get(pk=self.kwargs['classpk']))


class GetDiscussionResponses(generics.ListCreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrStudent)

    def get_queryset(self):
        return Response.objects.filter(discussion=self.kwargs['pk']).select_related('by')

    def perform_create(self, serializer):
        serializer.save(by=self.request.user, discussion=Discussion.objects.get(pk=self.kwargs['pk']))


class MarkDiscussionSolved(generics.UpdateAPIView):
    serializer_class = SolvedSerializer

    def get_queryset(self):
        return Discussion.objects.filter(created_by=self.request.user).select_related('created_by')
