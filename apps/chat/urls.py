# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path('save_message/', views.save_message, name='save_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
]