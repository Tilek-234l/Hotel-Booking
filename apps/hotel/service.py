# from django.db import models
# from django_filters import filters, FilterSet
#
# from .models import Room
#
#
# class RoomFilter(FilterSet):
#     class Meta:
#         model = Room
#         fields = {
#             'image': ['exact'],
#         }
#         filter_overrides = {
#             models.ImageField: {
#                 'filter_class': filters.CharFilter,
#                 'extra': lambda f: {
#                     'lookup_expr': 'exact',
#                 },
#             },
#         }
