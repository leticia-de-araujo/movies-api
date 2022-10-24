from django.urls import path

from .views import UserListDetailView, UserListView, UserView, UserLoginView

urlpatterns = [
    path("users/register/", UserView.as_view()),
    path("users/login/", UserLoginView.as_view()),
    path("users/", UserListView.as_view()),
    path("users/<int:user_id>/", UserListDetailView.as_view()),
]
