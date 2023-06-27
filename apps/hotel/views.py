from venv import logger

from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Review, Rating, RoomType, Room
from .permissions import IsOwnerOrReadOnly
from .serializers import ReviewCreateSerializer, CreateRatingSerializer, RoomDetailSerializer, RoomListSerializer, RoomSerializer
from rest_framework import generics, permissions, status
import logging
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from .serializers import RoomSerializer


class RoomListView(generics.ListAPIView):
    """Вывод списка типов комнат"""
    serializer_class = RoomListSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Room.objects.all(
        )
        return queryset


class RoomDetailView(generics.RetrieveDestroyAPIView):
    """Детальный вывод типа комнаты"""
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


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
            ).filter(booking__check_out_date__gte=timezone.now())

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(room=self.get_room())

    def get_room(self):
        room_id = self.kwargs.get('room_id')
        room = Room.objects.get(id=room_id)
        return room


class RoomViewSet(generics.CreateAPIView):
    queryset = Room.objects.order_by('id')
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


