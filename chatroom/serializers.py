from rest_framework import serializers
from .models import Topic,Room,Message
from users.serializers import UserSerializer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title']

class RoomSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    
    class Meta:
        model = Room
        fields = "__all__"
        depth = 5

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"