from genres.models import Genre
from genres.serializers import GenreSerializer
from .models import Movie

from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict) -> Movie:
        genres_data = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres_data:
            genre_dict = dict(genre)

            genre, _ = Genre.objects.get_or_create(**genre_dict)

            genre.movies.add(movie)

        return movie
