from rest_framework import serializers
from .models import User, UserProfile, UserTransactionTable, UserTestInfo, Account
import re

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data    
        


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user_address',
            'user_phone',
            'user_converted',
            'user_father_name',
            'user_dob',
            'user_budget',
            'user_college_preference',
            'user_profile_image',
            'user_created_at',
        ]
        

    def validate_user_phone(self, value):
            """
             Validates that the phone number is a valid Indian phone number.
            """
            phone_regex = r'^\+?91?[-\s]?\d{10}$'

            
            if not value:
                return value
            
            elif not re.match(phone_regex, value):
                raise serializers.ValidationError("Phone number must be a valid Indian phone number.")
            return value


class UserTransactionTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransactionTable
        fields = [
            'id',
            'user_payment_date',
            'user_amount',
            'user_transaction_type',
        ]


class UserTestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestInfo
        fields = [
            'id',
            'user_test_type',
            'user_test_score',
            'user_test_date',
            'user_test_exp_date',
            'user_test_document_image',
        ]


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_profile = UserProfileSerializer()
    user_test_info = UserTestInfoSerializer()
    is_email_verified = serializers.BooleanField(source='user.is_email_verified',read_only= True)
    is_profile_complete = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id',
            'user',
            'user_profile',
            'user_test_info',
            'is_email_verified',
            'is_profile_complete'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_profile_data = validated_data.pop('user_profile')
        user_test_info_data = validated_data.pop('user_test_info')

       

        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **user_profile_data)
        user_test_info = UserTestInfo.objects.create(user=user, **user_test_info_data)
        

        account = Account.objects.create(user=user, user_profile=user_profile, user_test_info=user_test_info, **validated_data)
        
        return account

    def update(self, instance, validated_data):
       
        user_data = validated_data.pop('user', None)
        user_profile_data = validated_data.pop('user_profile', None)
        user_test_info_data = validated_data.pop('user_test_info', None)

        password_exists= user_data.get("password")
        if password_exists:
            password= user_data.pop("password")
        if user_data:
            user = instance.user
            if password_exists:
                user.set_password(password)


            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        if user_profile_data:
            user_profile = instance.user_profile
            user_profile_serializer = UserProfileSerializer(user_profile, data=user_profile_data, partial=True)
            if user_profile_serializer.is_valid():
                user_profile_serializer.save()

        if user_test_info_data:
            user_test_info = instance.user_test_info
            user_test_info_serializer = UserTestInfoSerializer(user_test_info, data=user_test_info_data, partial=True)
            if user_test_info_serializer.is_valid():
                user_test_info_serializer.save()

        account = super().update(instance, validated_data)
        return account
    
    def get_is_email_verified(self, instance):
        return instance.user.is_email_verified

    def get_is_profile_complete(self, instance):
        return bool(instance.user.userprofile.user_phone)
    