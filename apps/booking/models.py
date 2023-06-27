from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.hotel.models import Room

User = get_user_model()


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_('User'),
        default=1
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_('Room'),
    )
    checkin_date = models.DateField(
        _('Check-in date'),
        null=True,
        blank=True
    )
    checkout_date = models.DateField(
        _('Checkout date'),
        null=True,
        blank=True
    )
    is_booked = models.BooleanField(
        _("Is Booked"),
        default=True
    )
    created_at = models.DateTimeField(_('Created at'), default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.room.room_number}"

    def charge(self) -> float:
        return (self.checkout_date - self.checkin_date + timedelta(1)).days * self.room.price

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")


