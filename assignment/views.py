from django.db.models import Count, Q
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from material.permissions import IsTeacherOrStudent
from . import serializers
from .permissions import IsTeacher, IsStudent
from .models import Assignment, GradedAssignment


class AssignmentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.AssignmentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assignment.objects \
            .filter(Q(classroom__students__in=[self.request.user]) | Q(classroom__created_by=self.request.user)) \
            .distinct() \
            .prefetch_related('questions')

    @action(detail=True, url_path='list', methods=['get'], permission_classes=[IsAuthenticated, IsTeacherOrStudent])
    def list_assignments(self, request, pk):
        obs = Assignment.objects.filter(classroom__id=pk).annotate(num_questions=Count('questions')).order_by(
            '-created_on')
        serializer = serializers.AssignmentSerializer(obs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher])
    def responses(self, request, pk):
        obs = GradedAssignment.objects.filter(assignment__id=pk).select_related('user').order_by('-marks', 'submitted')
        serializer = serializers.GradedAssignmentSerializer(obs, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes=[IsAuthenticated, IsStudent], methods=['post'],
            serializer_class=serializers.GradedAssignmentSerializer)
    def submit(self, request, pk):
        serializer = serializers.GradedAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(a_pk=pk, user=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[IsAuthenticated], methods=['get'])
    def graded(self, request, pk):
        obs = GradedAssignment.objects.filter(assignment__classroom__id=pk, user=request.user).order_by('-assignment')
        serializer = serializers.GradedAssignmentSerializer(obs, many=True)
        return Response(serializer.data)
