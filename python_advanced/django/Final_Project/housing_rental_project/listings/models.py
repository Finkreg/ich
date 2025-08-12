from django.db import models
from django.conf import settings # Import settings for USER model reference
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Listing(models.Model):
    # I'm binding the adverisement with the user that created it
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length = 255, verbose_name="ad title")
    description = models.TextField(verbose_name='description')
    location = models.CharField(max_length=255, verbose_name='location (city/region)')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price for one night')
    number_of_rooms = models.IntegerField(verbose_name='Number of rooms')

    HOUSING_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('room', 'Room'),
        ('other', 'Other'),
    ]
    housing_type = models.CharField(max_length=25, choices=HOUSING_TYPES, default='apartment', verbose_name='Housing type')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updated')
    views_count = models.IntegerField(default=0, verbose_name='Views count')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'
        ordering = ['-created_at']


class Booking (models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField(verbose_name='Booking start date')
    end_date = models.DateField(verbose_name='Booking end date')

    #Booking statuses
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending', verbose_name='Booking status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Booking creatiion date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Booking last updade date')


    def __str__(self):
        return f"Booking{self.listing.title} by {self.tenant.username} from {self.start_date} to {self.end_date}"
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        #to make sure one user cannot book the same advertisement:
        unique_together = ('listing', 'tenant', 'start_date', 'end_date')
        ordering = ['-created_at']


    
class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Rating (1 to 5)'
    )
    comment = models.TextField(blank=True, null=True, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Review creation date')


    def __str__(self):
        return f"Review on{self.listing.title} by {self.reviewer.username}"
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        #to make sure one user leaves only one review to one advertisement
        unique_together = ('listing', 'reviewer')
        ordering = ['-created_at']


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=255, verbose_name='Search query')
    searched_at = models.DateTimeField(auto_now_add=True, verbose_name='Date and time of a search')

    def __str__(self):
        return f'search{self.query} from {self.user.username}'
    
    class Meta:
        verbose_name = 'Search history'
        ordering = ['-searched_at']



class ViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='view_history', null=True, blank=True) 
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Date and time of view")

    def __str__(self):
        user_info = self.user.username if self.user else "Unauthenticated"
        return f"Viewed {self.listing.title} by user {user_info} at {self.viewed_at}"

    class Meta:
        verbose_name = "View history"
        verbose_name_plural = "View History"
        ordering = ['-viewed_at']
