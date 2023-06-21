from django.db import models
from django.db.models import Avg
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review, Rating, RoomType, Room
from .serializers import ReviewCreateSerializer, CreateRatingSerializer, RoomDetailSerializer, \
    RoomListSerializer, RoomSerializer


class RoomListView(generics.ListAPIView):
    """Вывод списка типов комнат"""
    serializer_class = RoomListSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Room.objects.annotate(
            middle_star=Avg('ratings__star')
        )
        return queryset


class RoomDetailView(generics.RetrieveAPIView):
    """Детальный вывод типа комнаты"""
    queryset = Room.objects.filter()
    serializer_class = RoomDetailSerializer

    def get_queryset(self):
        queryset = Room.objects.annotate(
            middle_star=Avg('ratings__star')
        )
        return queryset


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        check_in_date = self.request.query_params.get('check_in_date')
        check_out_date = self.request.query_params.get('check_out_date')

        if check_in_date and check_out_date:
            return Room.objects.exclude(
                booking__check_out_date__gte=check_in_date,
                booking__check_in_date__lte=check_out_date
            )
        return Room.objects.all()


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к отелю"""
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга отелю"""
    serializer_class = CreateRatingSerializer
    queryset = Rating.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(room=self.get_room())

    def get_room(self):
        room_id = self.kwargs.get('room_id')
        room = Room.objects.get(id=room_id)
        return room
