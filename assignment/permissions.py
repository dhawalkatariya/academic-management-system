from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q
from .models import Assignment


class IsTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        if pk is None:
            return True
        cls = Assignment.objects \
            .filter(Q(classroom__students__in=[request.user]) | Q(classroom__created_by=request.user), pk=pk) \
            .distinct() \
            .select_related('classroom')
        if cls and (request.method in SAFE_METHODS or cls[0].classroom.created_by == request.user.id):
            return True
        return False


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        if Assignment.objects.filter(pk=pk, classroom__created_by=request.user).exists():
            return True
        return False


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        if Assignment.objects.filter(pk=pk, classroom__students__in=[request.user]).exists():
            return True
        return False
