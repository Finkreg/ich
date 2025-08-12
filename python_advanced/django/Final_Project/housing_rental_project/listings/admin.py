from django.contrib import admin
from .models import Listing, Booking, Review, SearchHistory, ViewHistory

# Register your models here.
admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(SearchHistory)
admin.site.register(ViewHistory)

