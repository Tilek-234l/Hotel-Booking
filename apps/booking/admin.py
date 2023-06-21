from django.contrib import admin

from apps.booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", 'user', "checkin_date", "checkout_date", )
    list_per_page = 10
