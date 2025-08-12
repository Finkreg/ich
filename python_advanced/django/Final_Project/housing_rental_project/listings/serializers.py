from rest_framework import serializers
from .models import Listing, Review, Booking

class ListingSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at', 'views_count') 

    def create(self, validated_data):
        #redefine the method so that the current user automaticaly becomes an owner after creatinf the ad
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
        
class ListingDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at', 'views_count')

    
    def get_reviews(self, obj):
        #get the linked reviews for this ad
        #before we get approval we show all reviews
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer', 'listing', 'created_at')

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        validated_data['listing_id'] = self.context['view'].kwargs['listing_pk']
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    tenant_username = serializers.CharField(source='tenant.username', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'listing',
            'listing_title',
            'tenant',
            'tenant_username',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('tenant', 'status', 'created_at', 'updated_at')
    
    def validate(self, data):
        """to check whether end date is not earlier than booking date"""
        start_date = data['start_date']
        end_date = data['end_date']
        listing = data['listing']

        if start_date >= end_date:
            raise serializers.ValidationError('End date should be later than booking date')
        
        #check to see whether  approved booking dates overlap
        #exclude actual booking if that is an update
        if self.instance:
            existing_bookings = Booking.objects.filter(
                listing =listing,
                status='confirmed',
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exclude(pk=self.instance.pk)
        else:            
            existing_bookings = Booking.objects.filter(
                listing =listing,
                status='confirmed',
                start_date__lt=end_date,
                end_date__gt=start_date
            )
        if existing_bookings.exists():
            raise serializers.ValidationError("selected dates overlap with already existing dates")
        
        return data
