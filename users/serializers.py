from .models import User

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=127)
    birthdate = serializers.DateField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    bio = serializers.CharField(required=False)
    is_critic = serializers.BooleanField(required=False)

    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_email(self, value):
        email_already_exists = User.objects.filter(email=value).exists()

        if email_already_exists:
            raise serializers.ValidationError(detail="email already exists")

        return value

    def validate_username(self, value):
        username_already_exists = User.objects.filter(username=value).exists()

        if username_already_exists:
            raise serializers.ValidationError(detail="username already exists")

        return value

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(write_only=True)


class UserReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
