from rest_framework.views import APIView, Request, Response, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import User
from .permissions import isAdmin, isAccountOwnerOrAdmin
from .serializers import UserSerializer, UserLoginSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                {"detail": "invalid username or password"},
                status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class UserListView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdmin]

    def get(self, request: Request) -> Response:
        users = User.objects.all()

        result_page = self.paginate_queryset(users, request, view=self)

        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserListDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAccountOwnerOrAdmin]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)
