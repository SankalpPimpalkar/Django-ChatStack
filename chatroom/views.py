from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TopicSerializer,RoomSerializer,MessageSerializer
from rest_framework.exceptions import AuthenticationFailed,NotFound
from users.models import User
from .models import Room,Topic,Message
import jwt

# Create your views here.
class CreateTopic(APIView):
    def post(self,request):
        serializer = TopicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'New topic created successfully',
            'success': True
        })

class GetTopics(APIView):
    def get(self,request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        
        return Response({
            'message': 'Fetched topics successfully',
            'success': True,
            'data': serializer.data
        })

class CreateRoom(APIView):
    def post(self, request):
        token = request.COOKIES.get('token')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'SECRET',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token or Expired token')
        
        user = User.objects.filter(id=payload.get('id')).first()

        if user is None:
            raise AuthenticationFailed('User does not exist')
        
        room = Room.objects.create(
            owner= user
        )
        
        for key,value in request.data.items():
            if value is not None:
                if hasattr(room,key) and key != 'topic':
                    setattr(room, key, value)
        
        topic = Topic.objects.filter(title= request.data['topic']).first()
        print(topic)

        if topic is None:
            raise NotFound('Topic does not exist')
        
        room.topic = topic
        room.owner = user
        room.save()
        
        serializer = RoomSerializer(room)

        return Response({
            'message': 'New Room has been created',
            'success': True,
            'data': serializer.data
        })