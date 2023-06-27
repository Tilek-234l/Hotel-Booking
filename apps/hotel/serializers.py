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
    """Список отелей"""
    room_type_name = serializers.CharField(source='room_type.name')
    room_number = serializers.CharField()
    price = serializers.IntegerField()
    is_booked = serializers.SerializerMethodField()
    middle_star = serializers.IntegerField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "room_type_name", "room_number", "price", "is_booked", "middle_star", "img")

    def get_is_booked(self, obj):
        if obj.is_booked:
            return False
        return True

    def get_img(self, obj):
        request = self.context.get('request')
        room_photos = obj.roomphotos_set.all()
        if room_photos:
            image_url = room_photos[0].image.url
            full_url = request.build_absolute_uri(image_url)
            return full_url
        return None



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
    """Детальный вид номера"""
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
