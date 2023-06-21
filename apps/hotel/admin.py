from django import forms
from django.contrib import admin

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from apps.hotel.models import Room, RoomType, Review, Rating, RatingStar, RoomPhotos, Hotel


class RoomAdminForm(forms.ModelForm):
    description = forms.CharField(
        label="Description",
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Room
        fields = '__all__'


class RoomPhotosInline(admin.TabularInline):
    model = RoomPhotos
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height= "110"')

    get_image.short_description = _("Image")


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = (
        "name",
    )


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'description',
    )


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'room_type',
        'room_number',
        'price',
        'is_booked',

    )
    save_on_top = True
    inlines = [RoomPhotosInline, ReviewInline, RatingInline, ]
    form = RoomAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "room",
        "id"
    )
    readonly_fields = (
        "name",
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "star",
        'room',
    )


@admin.register(RoomPhotos)
class RoomPhotosAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "get_image"
    )
    readonly_fields = (
        "get_image",
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = _("Image")


admin.site.register(RatingStar)
