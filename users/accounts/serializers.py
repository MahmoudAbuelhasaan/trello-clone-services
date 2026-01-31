from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth.password_validation import validate_password

class UserRigisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        help_text="Password must be at least 8 characters long.")
    password_confirm = serializers.CharField(write_only=True, required=True,  help_text="Password must be at least 8 characters long.")

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_email(self, value):
        """Validate that the email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        """Validate that the username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    def validate(self, data):
        """Validate that the two password fields match."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        validate_password(data['password'])
        return data 
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        # fields = '__all__'
        # execlode password from serialization
        exclude = ('password','is_superuser','is_staff','is_active','groups','user_permissions')

        read_only_fields = ('id', 'date_joined', 'last_login')
        
    