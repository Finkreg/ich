from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import ListingViewSet, ReviewViewSet, BookingViewSet

#Main Router
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing') #/listings/, /listings/{id}/
router.register(r'bookings', BookingViewSet, basename='booking')

#Nested Router for reviews (linked to listings)
#/listings/{listing_pk}/reviews/
listings_router = routers.NestedSimpleRouter(router, r'listings', lookup='listing')
listings_router.register(r'reviews', ReviewViewSet, basename='listing-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(listings_router.urls)),
]


