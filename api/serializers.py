from rest_framework import serializers
from .models import StoryRequest

class StoryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRequest
        fields = '__all__'
