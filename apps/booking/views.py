from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, permissions
from .serializers import BookingSerializer
from .models import Booking
from apps.hotel.models import Room
from rest_framework.exceptions import ValidationError


class BookingRoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'price', 'room_type']


class BookingCreateViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        room = serializer.validated_data['room']

        # Проверяем, доступен ли номер комнаты для бронирования
        if room.is_booked:
            raise ValidationError("The room is already booked.")

        # Устанавливаем значение is_booked в True
        room.is_booked = True
        room.save()

        # Сохраняем бронирование
        serializer.save(
            user=self.request.user,
        )


class BookingCreateAPIView(BookingCreateViewSet):
    def create_booking(self, request):
        room_id = 1  # ID комнаты, которую хотите забронировать
        room = Room.objects.get(id=room_id)
        booking = Booking.objects.create(room=room)

        # Дополнительные действия при создании бронирования
        # Например, отправка уведомления пользователю о бронировании

        # Получаем доступные комнаты и даты для бронирования
        available_rooms, available_dates = booking.get_available_rooms()

        # Возвращаем ответ с информацией о созданном бронировании и доступных комнатах/датах
        serializer = self.get_serializer(booking)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {
                'booking': serializer.data,
                'available_rooms': available_rooms,
                'available_dates': available_dates,
            },
            status=status.HTTP_201_CREATED
        )

