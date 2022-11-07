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

            genre_obj, _ = Genre.objects.get_or_create(**genre_dict)

            genre_obj.movies.add(movie)

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:

        for key, value in validated_data.items():
            if key == "genres":
                genres = Genre.objects.all()

                new_movies = [instance]

                for old_genre in genres:
                    if old_genre.movies.filter(id=instance.id):
                        old_genre.movies.clear()

                for genre in value:
                    genre_dict = dict(genre)

                    genre_obj, _ = Genre.objects.get_or_create(**genre_dict)

                    genre_obj.movies.set(new_movies)

            else:
                setattr(instance, key, value)

        instance.save()

        return instance
