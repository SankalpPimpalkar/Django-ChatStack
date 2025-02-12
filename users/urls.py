from django.urls import path
from .views import Register,Login,UserDetails,Logout

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('user', UserDetails.as_view()),
    path('logout', Logout.as_view()),
]
