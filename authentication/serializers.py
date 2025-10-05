from rest_framework import serializers
from .models import User
import re


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration"""
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    patronymic = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True)

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        
        # Additional email format validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format")
        
        return value.lower()

    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        return value

    def validate(self, data):
        """Validate password confirmation"""
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })
        return data

    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'patronymic', 
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic']
