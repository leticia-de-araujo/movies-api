from django.urls import path
from .views import MovieView, MovieDetailView
from reviews.views import ReviewView, ReviewDetailView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieDetailView.as_view()),
    path("movies/<int:movie_id>/reviews/", ReviewView.as_view()),
    path(
        "movies/<int:movie_id>/reviews/<int:review_id>/",
        ReviewDetailView.as_view(),
    ),
]
