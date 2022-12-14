from rest_framework.permissions import BasePermission
from django.db.models import Q
from classroom.models import Class


class IsTeacherOrStudent(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        if Class.objects \
                .filter(Q(students__in=[request.user]) | Q(created_by=request.user), pk=pk) \
                .exists():
            return True
        return False
