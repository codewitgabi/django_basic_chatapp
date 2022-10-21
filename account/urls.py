from django.urls import path
from . import views


urlpatterns = [
    path('', views.signup, name= 'signup'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('chat/', views.chat, name= 'chat'),
    path('send-message/', views.sendMessage, name= 'send_message'),
    path('get-message/', views.getMessage, name= 'get_message'),
]