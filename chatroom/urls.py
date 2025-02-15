from django.urls import path
from .views import *

urlpatterns = [
    path('create-topic', CreateTopic.as_view()),
    path('get-topics', GetTopics.as_view()),
    
    path('create-room', CreateRoom.as_view()),
    path('get-rooms', GetRooms.as_view()),
    
    path('create-message', CreateMessage.as_view()),
    path('get-messages', GetMessages.as_view()),
]
