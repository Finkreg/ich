import django_filters
from .models import Listing
from django.db import models

class ListingFilter(django_filters.FilterSet):
    """Filtration class for Listing model. Allows search and filter the ads"""

    #Keyword search
    search = django_filters.CharFilter(method='filter_search', label='search by keywords')

    #Price filtration
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte', label='min price')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte', label='max price')

    #amount of rooms filtration
    min_rooms = django_filters.NumberFilter(field_name='number_of_rooms', lookup_expr='gte', label='min room amount')
    max_rooms = django_filters.NumberFilter(field_name='number_of_rooms', lookup_expr='lte', label='max room amount')

    #filtration by location
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='location')

    #filtration by housing type
    housing_type = django_filters.ChoiceFilter(choices=Listing.HOUSING_TYPES, label='housing types')


    class Meta:
        model = Listing
        fields = [
            'search',
            'min_price', 'max_price',
            'min_rooms', 'max_rooms',
            'location',
            'housing_type',
            'is_active',
        ]

    def filter_search(self, queryset, name, value):
        """method to search by keywords"""
        return queryset.filter(
            models.Q(title__icontains=value) | models.Q(description__icontains=value)
        )