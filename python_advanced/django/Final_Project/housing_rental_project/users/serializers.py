from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator
from listings.models import SearchHistory
from django.db import transaction

User = get_user_model() #getting the current active user model

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message='User with this email already registered.')]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="password should be complex"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Please repeat password"
    )

    is_landlord = serializers.BooleanField(
        required=False,
        default=False,
        write_only=True,
        help_text="mark this if you are registering as Landlord"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'is_landlord')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        """Check whether both passwords are the same"""
        if data['password'] != data['password2']: #the dictionary "data" already has the clear serialized passwords
            raise serializers.ValidationError({'password': 'passwords don\'t match'})
        return data
    
    def create(self, validated_data):
        """Creates the user after successful validation and adds it to Landlords group if that was selected"""
        is_landlord = validated_data.pop('is_landlord', False)
        validated_data.pop('password2')

        with transaction.atomic(): #I have to make sure that the transaction will execute in full 
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )

            if is_landlord:
                landlord_group, created = Group.objects.get_or_create(name='Landlords') #also let's check the Landlords group exists
                user.groups.add(landlord_group)
        return user


        """OLD LOGIC THAT DIDN'T ALLOW TO CHOOSE LANDLORD GROUP"""
        # user = User.objects.create_user(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     first_name=validated_data.get('first_name', ''),
        #     last_name=validated_data.get('last_name', ''),
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        # return user

class UserLoginSerializer(serializers.Serializer):
    """Login Serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory 
        fields = '__all__'
        read_only_fields = ('user', 'searched_at')