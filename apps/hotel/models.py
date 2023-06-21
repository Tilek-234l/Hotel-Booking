from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _


class Hotel(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50,
        null=True,
        blank=True,
        unique=True,
    )
    address = models.CharField(
        _("Address"),
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField(
        _("Description"),
        max_length=500,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        _("Hotels_Image"),
        upload_to="hotels/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")


class RoomType(models.Model):
    name = models.CharField(
        _("Room Type"),
        max_length=50,
        null=True,
        blank=True,
    )

    description = models.TextField(
        _("Description"),
        max_length=500,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Room Type")
        verbose_name_plural = _("Room Types")


class Room(models.Model):
    room_type = models.ForeignKey(
        'RoomType',
        on_delete=models.CASCADE
    )
    room_number = models.CharField(
        _("Room Number"),
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )
    price = models.PositiveIntegerField(
        _("Price"),
    )
    is_booked = models.BooleanField(
        _("Is Booked"),
        default=False
    )

    def __str__(self):
        return f"Room {self.room_number} at {self.room_type.name}"

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class RoomPhotos(models.Model):
    image = models.ImageField(
        _('Room Photo'),
        upload_to='room_photos/'
    )
    room = models.ForeignKey(
        Room,
        verbose_name='Room',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Room Photo')
        verbose_name_plural = _('Room Photos')


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(
        _('Value'),
        default=0
    )

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = _("Rating Star")
        verbose_name_plural = _("Rating Stars")
        ordering = ["-value"]


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        default=None
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name='star'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="room",
        related_name="ratings",
        default=0
    )

    def __str__(self):
        return f"{self.star} - {self.room}"

    class Meta:
        unique_together = (("user", "room"),)
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")


class Review(models.Model):
    email = models.EmailField(
        blank=True,
        null=True
    )
    name = models.CharField(
        _("Name"),
        max_length=100
    )
    text = models.TextField(
        _("Text"),
        max_length=5000
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=_("Parent"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    room = models.ForeignKey(
        Room,
        verbose_name="room",
        on_delete=models.CASCADE,
        related_name="reviews",
        default=None,
    )

    def __str__(self):
        return f"{self.name} - {self.room}"

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')