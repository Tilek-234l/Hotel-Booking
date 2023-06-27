from rest_framework import serializers

from .models import Review, Rating, RoomType, Room


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data




class RoomListSerializer(serializers.ModelSerializer):
    room_type = serializers.CharField(source='room_type.name')
    room_number = serializers.CharField()
    price = serializers.IntegerField()
    is_booked = serializers.BooleanField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, room):
        if room.image:
            request = self.context.get('request')
            return request.build_absolute_uri(room.image.url)
        return None

    class Meta:
        model = Room
        fields = ('room_type', 'room_number', 'price', 'is_booked', 'image_url')



class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {
            'parent': {'required': False}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['name'] = user.get_full_name() or user.username
        validated_data['email'] = user.email
        review = Review.objects.create(**validated_data)
        return review


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыво"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("id", "name", "text", "children")


class RoomDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    average_rating = serializers.FloatField(source='middle_star')

    class Meta:
        model = Room
        fields = "__all__"


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "room")

    def create(self, validated_data):
        user = self.context['request'].user
        rating, _ = Rating.objects.update_or_create(
            user=user,
            room=validated_data.get('room', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


class RoomSerializer(serializers.ModelSerializer):
    room_type_name = serializers.ReadOnlyField(source='room_type.name')
    room_type_description = serializers.ReadOnlyField(source='room_type.description')

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'room_number', 'price', 'is_booked', 'room_type_name', 'room_type_description']
