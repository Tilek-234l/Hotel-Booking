from django.urls import path
from .views import BookingCreateViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'booking', BookingCreateViewSet)

urlpatterns = router.urls
