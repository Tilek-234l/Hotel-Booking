from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'checkin_date', 'checkout_date', ]
        read_only_fields = ['id', 'user', 'room']
