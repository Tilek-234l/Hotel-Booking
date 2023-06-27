from django.urls import path
from . import views

urlpatterns = [
    path("room/", views.RoomListView.as_view()),
    path("room/<int:pk>/", views.RoomDetailView.as_view(), name="room-detail"),
    path("review/", views.ReviewCreateView.as_view()),
    path("room/<int:room_id>/rating/", views.AddStarRatingView.as_view(), name="add_rating"),
    path("room-list/", views.RoomListAPIView.as_view()),
]
