from django.urls import path

from .views import API_Test, DishAPIView, IngredientFilterAPIView, EquipmentFilterAPIView, QuickRecipesAPIView, \
    ReviewCreateView, ReplyCreateView, SearchAPIView, CategoryAPIView, CuisineAPIView, ReviewLikeView, \
    BestRecipesAPIView, CuisineCategoryPageView
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    path("", TemplateView.as_view(template_name="dishes_list/index.html")),
    path("dish/<slug:slug>/", TemplateView.as_view(template_name="dish/index.html")),
    path("api/v1/", API_Test.as_view(), name="api_test"),
    path("api/v1/dish/<slug:slug>/", DishAPIView.as_view()),
    path("api/v1/cuisine/<int:cuisine_id>/", CuisineCategoryPageView.as_view(), name="cuisine-page"),
    path("api/v1/category/<int:category_id>/", CuisineCategoryPageView.as_view(), name="category-page"),

    path("api/v1/ingredient-filter/", IngredientFilterAPIView.as_view(), name="ing-filter"),
    path("api/v1/equipment-filter/", EquipmentFilterAPIView.as_view(), name="equip-filter"),
    path("api/v1/all-categories/", CategoryAPIView.as_view(), name="all-categories"),
    path("api/v1/all-cuisines/", CuisineAPIView.as_view(), name="all-cuisines"),

    path("api/v1/quick-recipes/", QuickRecipesAPIView.as_view(), name="quick-recipes"),
    path("api/v1/best-recipes/", BestRecipesAPIView.as_view(), name="best-recipes"),
    path("api/v1/search/", SearchAPIView.as_view(), name="search"),

    path('api/reviews/<int:dish_id>/create/', ReviewCreateView.as_view(), name='create_review'),
    path('api/reviews/<int:dish_id>/<int:parent_id>/reply/', ReplyCreateView.as_view(), name='create_reply'),

    path('api/reviews/<int:review_id>/like/', ReviewLikeView.as_view()),
]
