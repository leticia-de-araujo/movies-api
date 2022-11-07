from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from movies.models import Movie

from django.shortcuts import get_object_or_404

from .permissions import IsAdminOrCriticOrReadOnly, IsAdminOrReviewCriticOrReadOnly
from .serializers import ReviewSerializer
from .models import Review


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCriticOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:

        reviewAlreadyExists = Review.objects.filter(
            user_id=request.user.id, movie_id=movie_id
        )

        if reviewAlreadyExists:
            return Response(
                {"detail": "Review already exists."}, status.HTTP_403_FORBIDDEN
            )

        serializer = ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie_id=movie_id)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        reviews = Review.objects.filter(movie=movie)

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReviewCriticOrReadOnly]

    def get(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, id=review_id)

        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(
        self,
        request: Request,
        movie_id: int,
        review_id: int,
    ) -> Response:
        review = get_object_or_404(Review, id=review_id)

        self.check_object_permissions(request, review)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
