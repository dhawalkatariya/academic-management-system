from rest_framework import permissions
from .models import Class
from django.db.models import Q


class IsStudentOrTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        if Class.objects.filter(pk=pk).filter(Q(created_by=request.user) | Q(students__id=request.user.id)).exists():
            return True
        return False
