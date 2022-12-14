from rest_framework import serializers
from .models import Discussion, Response
from classroom.serializers import UserSerializer


class DiscussionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Discussion
        fields = '__all__'
        read_only_fields = ('solved', 'classroom')


class ResponseSerializer(serializers.ModelSerializer):
    by = UserSerializer(read_only=True)

    class Meta:
        model = Response
        fields = '__all__'
        read_only_fields = ['discussion']


class SolvedSerializer(serializers.ModelSerializer):
    class Meta(DiscussionSerializer.Meta):
        read_only_fields = ('id', 'created_by', 'question', 'classroom')
