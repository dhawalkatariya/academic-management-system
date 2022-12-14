from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacherOrStudent
from .models import Material
from .serializers import MaterialSerializer


class MaterialViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MaterialSerializer

    def get_queryset(self):
        return Material.objects.filter(classroom__created_by=self.request.user)

    @action(detail=True, url_path='list', methods=['get'], permission_classes=[IsAuthenticated, IsTeacherOrStudent])
    def list_material(self, request, pk):
        obs = Material.objects.filter(classroom__pk=pk)
        serializer = MaterialSerializer(obs, many=True)
        return Response(serializer.data)
