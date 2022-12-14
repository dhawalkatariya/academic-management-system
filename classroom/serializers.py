from rest_framework import serializers
from .models import Class
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')


class ClassSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ('id', 'created_by', 'name',
                  'invitation_code', 'created_on')
        read_only_fields = ('invitation_code', 'created_by')


class InvitationSerializer(serializers.Serializer):
    invitation_code = serializers.CharField(required=True, min_length=12, max_length=12)
