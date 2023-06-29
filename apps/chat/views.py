from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Message, Room


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    messages = Message.objects.all()
    return render(request, "chat/room.html", {"room_name": room_name, "messages": messages})


def chat_room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})


@csrf_exempt
def save_message(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        message = request.POST.get('message')
        room_name = request.POST.get('room_name')  # Add the room_name field to the form or pass it in the request
        room = Room.objects.get_or_create(room_name=room_name)
        Message.objects.create(room=room, username=username, message=message)
        return JsonResponse({'status': 'success'})


def get_messages(request):
    messages = Message.objects.all()
    data = [{'username': message.username, 'message': message.message} for message in messages]
    return JsonResponse(data, safe=False)
