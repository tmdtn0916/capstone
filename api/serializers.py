from rest_framework import serializers
from .models import StoryRequest, User

class StoryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRequest
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'phone']