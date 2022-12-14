from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q
from .models import Discussion
from classroom.models import Class


class IsStudentOrReadonly(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['classpk']
        cls = Class.objects \
            .filter(Q(students__in=[request.user]) | Q(created_by=request.user), pk=pk) \
            .distinct() \
            .select_related('created_by')
        if cls and (request.method in SAFE_METHODS or cls[0].created_by != request.user):
            return True
        return False


class IsTeacherOrStudent(BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        pk = view.kwargs['pk']
        if Discussion.objects \
                .filter(Q(classroom__students__in=[request.user]) | Q(classroom__created_by=request.user), pk=pk) \
                .exists():
            return True
        return False
