from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import datetime
import jwt

# Create your views here.
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            'expiry': str(datetime.datetime.now() + datetime.timedelta(days=5)),
            'created_at': str(datetime.datetime.now())
        }
        
        token = jwt.encode(payload, 'SECRET',algorithm='HS256')
        
        response =  Response()
        
        response.data = {
            'token':token,
            'message': 'User logged in successfully'
        }
        response.set_cookie('token', token, httponly=True)
        
        return response
    
class UserDetails(APIView):
    def get(self,request):
        token = request.COOKIES.get('token')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'SECRET',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token or Expired token')
        
        user = User.objects.get(id=payload.get('id'))
        
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'User logged out successfully'
        }
        
        return response