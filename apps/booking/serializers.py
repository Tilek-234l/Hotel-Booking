from rest_framework import serializers
from .models import Booking
from apps.hotel.models import Room


class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'price', 'room_type']


class BookingSerializer(serializers.ModelSerializer):
    room = BookingRoomSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'checkin_date', 'checkout_date', 'created_at']
