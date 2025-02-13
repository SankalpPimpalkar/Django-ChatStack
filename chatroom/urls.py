from django.urls import path
from .views import CreateTopic,CreateRoom,GetTopics

urlpatterns = [
    path('create-topic', CreateTopic.as_view()),
    path('get-topics', GetTopics.as_view()),
    
    path('create-room', CreateRoom.as_view()),
]
