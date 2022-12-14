from rest_framework import serializers
from classroom.models import Class
from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all().select_related('created_by'))

    def validate_classroom(self, value):
        if value.created_by.id == self.context['request'].user.id:
            return value
        raise serializers.ValidationError("You cannot post material to this class.")

    class Meta:
        model = Material
        fields = ('id', 'arrived', 'message', 'attachment', 'url', 'classroom')
