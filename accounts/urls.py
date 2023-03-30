from django.urls import path, include
from django.views.generic import TemplateView
from djoser.views import TokenCreateView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from accounts.views import UserProfileView, CreateList_of_DishAPIView, activate, AddFavoriteRecipeAPIView, \
    FavoriteRecipesAPIView, user_activation, UserRegistrationView, RemoveFavoriteRecipeAPIView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
    path('auth/token/', TokenCreateView.as_view(), name='token_create'),

    path('regform/', TemplateView.as_view(template_name="forms/registration.html")),
    path('register/', UserRegistrationView.as_view(), name='register'),

    # path("activate/<uid>/<token>/", activate, name='activate'),
    path('activate/<uidb64>/<token>/', user_activation, name='activate'),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),

    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path("api/add_to_favorites/<int:dish_id>/", AddFavoriteRecipeAPIView.as_view(), name="add_to_favorite"),
    path('api/favorite/<int:dish_id>/remove/', RemoveFavoriteRecipeAPIView.as_view()),
    path("api/user_favorites/", FavoriteRecipesAPIView.as_view(), name="user_favorites"),

    path("api/add_dish/", CreateList_of_DishAPIView.as_view(), name="add_dish")

]
