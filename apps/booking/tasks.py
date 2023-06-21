from celery import shared_task
from datetime import date
from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
def check_checkout_dates():
    today = date.today()
    users = User.objects.filter(booking__checkout_date=today)
    admin_email = 'snoopdas@mail.ru'  # Замените на адрес электронной почты вашего администратора
    message = f"Today is the checkout date for the following bookings: {users}"
    send_mail('Checkout Date Reminder', message, 'noreply@example.com', [admin_email])
