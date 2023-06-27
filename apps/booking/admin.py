from django.contrib import admin

from apps.booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "checkin_date", "checkout_date", 'created_at', 'is_booked',)
    list_per_page = 10
