from rest_framework import serializers

from base.models import List_of_Dish
from .models import UserProfile, FavoriteRecipe
from djoser.serializers import TokenSerializer
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        # Create a new User object with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Update the existing UserProfile object linked to the user,
        # or create a new one if it doesn't exist yet
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        return user

    def validate_email(self, value):
        # Check if email is already registered
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already registered.')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'description', 'avatar', 'email', 'is_email_verified']


class CustomTokenSerializer(TokenSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        token['profile'] = {
            'url': '/api/profile/',
        }
        return token


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'dish', 'dish_name', 'user']


class CreateList_of_Dish_Serializer(serializers.ModelSerializer):
    class Meta:
        model = List_of_Dish
        fields = ("name", "image", "description", "time", "time_min", "url", "priority",
                  "instruction", "ingredient", "equipment", "cuisine", "category",
                  'fats', 'carbohydrates')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)