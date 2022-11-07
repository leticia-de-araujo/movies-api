from rest_framework import serializers
from .models import Review

from users.serializers import UserReviewSerializer
from movies.models import Movie
from users.models import User

from django.shortcuts import get_object_or_404


class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)
    stars = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "user",
            "movie_id",
        ]

        read_only_fields = ["movie_id"]

    def create(self, validated_data: dict) -> Review:
        movie_id = validated_data.pop("movie_id")
        user = validated_data.pop("user")

        movie_obj = get_object_or_404(Movie, id=movie_id)
        user_obj = get_object_or_404(User, id=user.id)

        validated_data["movie"] = movie_obj
        validated_data["user"] = user_obj

        review = Review.objects.create(**validated_data)

        return review
