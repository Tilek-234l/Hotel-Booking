from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        null=True
    )
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        null=True

    )
    email = models.EmailField(
        _("email address"),
        blank=True,
        null=True,
        unique=True

    )
    phone_number = PhoneNumberField(
        _("phone number"),
        null=True,
        blank=True,
        default=None,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)