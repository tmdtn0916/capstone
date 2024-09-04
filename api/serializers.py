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

    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user