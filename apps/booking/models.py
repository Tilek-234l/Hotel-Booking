from datetime import timedelta
from django.utils import timezone


from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.hotel.models import Room

User = get_user_model()


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='booking',
        verbose_name=_('User'),
        default=1
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='booking',
        verbose_name=_('Room'),
    )
    checkin_date = models.DateField(
        _('Checkin date'),
        default=timezone.now
    )
    checkout_date = models.DateField(
        _('Checkout date'),
        default=timezone.now
    )

    def __str__(self):
        return f"{self.user.username} - {self.room.room_number}"

    def charge(self) -> float:
        return (self.checkout_date - self.checkin_date + timedelta(1)).days * self.room.price

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")


