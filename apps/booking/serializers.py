from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'checkin_date', 'checkout_date', 'created_at']
        read_only_fields = ['id', 'user', 'room', 'created_at']

