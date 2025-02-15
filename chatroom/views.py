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

class GetRooms(APIView):
    def get(self, request):
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
        
        topic_type = request.GET.get('topic')
        
        rooms = Room.objects.all()
        
        if topic_type:
            rooms = Room.objects.filter(topic__title=topic_type)
        serialize = RoomSerializer(rooms, many=True)

        return Response({
            'message': 'Rooms fetched successfully',
            'success': True,
            'data': serialize.data,
            'rooms_count': len(serialize.data)
        })

class CreateMessage(APIView):
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
        
        body = request.data['body']
        room = Room.objects.filter(id=request.GET.get('room')).first()

        if room is None:
            raise NotFound('Room not found')

        message = Message.objects.create(
            body=body,
            user=user,
            room=room
        )
        
        serialize = MessageSerializer(message)
        
        return Response({
            'message': 'Message created',
            'success': True,
            'data': serialize.data
        })

class GetMessages(APIView):
    def get(self, request):
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
        
        room_id = request.GET.get('room')
        
        if not room_id:
            return Response({
                'message': 'Room Id is required',
                'success': False
            })
        
        room = Room.objects.filter(id=room_id).first()
        messages = room.messages.all()

        message_serializer = MessageSerializer(messages, many=True)
        
        return Response({
            'message': 'Messages fetched successfully',
            'success': True,
            'data': message_serializer.data
        })