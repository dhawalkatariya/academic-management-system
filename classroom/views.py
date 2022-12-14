from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Class
from .serializers import ClassSerializer, UserSerializer, InvitationSerializer
from .permissions import IsStudentOrTeacher


# Create your views here.

class ClassViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()

    def get_queryset(self):
        return self.request.user.created_classes.order_by('name').select_related('created_by')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def joined(self, request):
        qs = request.user.joined_classes.order_by('name').select_related('created_by')
        serializer = ClassSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], serializer_class=InvitationSerializer)
    def join(self, request):
        code_serializer = InvitationSerializer(data=request.data)
        if code_serializer.is_valid():
            c = get_object_or_404(Class, ~Q(created_by=request.user), invitation_code=request.data['invitation_code'])
            c.students.add(request.user)
            serializer = ClassSerializer(c)
            return Response(serializer.data)
        else:
            return Response(code_serializer.errors, 400)

    @action(detail=True, methods=['get'], serializer_class=UserSerializer,
            permission_classes=[IsAuthenticated, IsStudentOrTeacher])
    def students(self, request, pk=None):
        c = get_object_or_404(Class.objects.prefetch_related('students'), pk=pk)
        serializer = UserSerializer(c.students, many=True)
        return Response(serializer.data)
