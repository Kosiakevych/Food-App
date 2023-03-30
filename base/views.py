from random import shuffle
from rest_framework import status, permissions
from .filters import filter_dish
from .models import List_of_Dish, Equipment, All_Ingredients, Reviews, Cuisine, Category, ReviewImages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import List_of_Dish_Serializer, Dish_Serializer, IngredientFilterSerializer, \
    EquipmentFilterSerializer, ReviewSerializer, CuisineSerializer, CategorySerializer
from fuzzywuzzy import fuzz
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from change_file_name import handle_uploaded_file

all_dish = List_of_Dish.objects.all()


class API_Test(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of dishes",
        operation_description="<b>Returns a paginated list of dishes. "
                              "The offset parameter specifies the number of dishes that already loaded. "
                              "It is needed for infinity scroll. "
                              "From number that in offset to offset + 9. "
                              "If the offset parameter is not specified, it defaults to 0.</b>",
        manual_parameters=[
            openapi.Parameter('offset', openapi.IN_QUERY, description="The number of dishes that need to upload.",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('equipment', openapi.IN_QUERY,
                              description="A comma-separated list of equipment names to filter the dishes by.",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ingredient', openapi.IN_QUERY,
                              description="A comma-separated list of ingredient names to filter the dishes by.",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('time_min', openapi.IN_QUERY,
                              description="The maximum time (in minutes) required to prepare a dish.",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: List_of_Dish_Serializer(many=True)},
        tags=["Pages"])
    def get(self, request):
        offset = int(request.GET.get('offset', 0))  # if no request offset -> int(NoneType) so -> 0
        queryset = filter_dish(request)
        if queryset is False:
            serializer = List_of_Dish_Serializer(all_dish[offset:offset + 9], many=True, context={'request': request})
            return Response(serializer.data)
        serializer = List_of_Dish_Serializer(queryset[offset:offset + 9], many=True, context={'request': request})
        return Response(serializer.data)


class DishAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get a dish by slug",
        operation_description="<b>Retrieve a single dish by its unique slug.</b>",
        responses={200: Dish_Serializer()},
        tags=["Pages"])
    def get(self, request, slug):
        try:
            dish = List_of_Dish.objects.get(url=slug)
            serializer = Dish_Serializer(dish, context={'request': request})
            return Response(serializer.data)
        except List_of_Dish.DoesNotExist:
            return Response({'error': 'Dish not found'}, status=status.HTTP_404_NOT_FOUND)


class IngredientFilterAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of all ingredients",
        responses={200: IngredientFilterSerializer(many=True)},
        tags=["Get Info"])
    def get(self, request):
        all_ing = All_Ingredients.objects.all()
        serializer = IngredientFilterSerializer(all_ing, many=True)
        return Response(serializer.data)


class EquipmentFilterAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of all equipment",
        responses={200: EquipmentFilterSerializer(many=True)},
        tags=["Get Info"])
    def get(self, request):
        all_equip = Equipment.objects.all()
        serializer = EquipmentFilterSerializer(all_equip, many=True)
        return Response(serializer.data)


class CuisineAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of all cuisines",
        responses={200: CuisineSerializer(many=True)},
        tags=["Get Info"])
    def get(self, request):
        all_cuisine = Cuisine.objects.all()
        serializer = CuisineSerializer(all_cuisine, many=True)
        return Response(serializer.data)


class CategoryAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of all categories",
        responses={200: CategorySerializer(many=True)},
        tags=["Get Info"])
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)


class SearchAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get 20 dish from search",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description='Search query text',
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: List_of_Dish_Serializer(many=True)},
        tags=["Recipes"])
    def get(self, request):
        search_text = request.GET.get('search')  # Get the search query from the request's query parameters
        matching_dishes = []
        # Iterate through each dish to find matching ones
        for dish in all_dish:
            # Calculate the partial ratio between the search query and the dish name,
            # using fuzzywuzzy's partial_ratio function. If the ratio is higher than 75,
            # consider the dish a match and add it to the list of matching dishes.
            if fuzz.partial_ratio(search_text.lower(), dish.name.lower()) > 75:
                matching_dishes.append(dish)
        serializer = List_of_Dish_Serializer(matching_dishes[:20], many=True)
        return Response(serializer.data)


class QuickRecipesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get quick recipes",
        responses={200: List_of_Dish_Serializer(many=True)},
        manual_parameters=[
            openapi.Parameter('offset', openapi.IN_QUERY, description="The number of dishes that need to upload.",
                              type=openapi.TYPE_INTEGER),
        ],
        tags=["Recipes"])
    def get(self, request):
        offset = int(request.GET.get('offset', 0))  # if no request offset -> int(NoneType) so -> 0
        quick_recipes = List_of_Dish.objects.filter(time_min__gte=5, time_min__lte=30)
        if quick_recipes.exists():
            quick_recipes = list(quick_recipes)
            shuffle(quick_recipes)
            serialized_recipes = List_of_Dish_Serializer(quick_recipes[offset:offset + 9], many=True)
            return Response(serialized_recipes.data)
        else:
            return Response({})


class BestRecipesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get best recipes",
        responses={200: List_of_Dish_Serializer(many=True)},
        tags=["Recipes"])
    def get(self, request):
        best_recipes = List_of_Dish.objects.filter(rating__gte=4.5)
        if best_recipes.exists():
            best_recipes = list(best_recipes)
            shuffle(best_recipes)
            serialized_recipes = List_of_Dish_Serializer(best_recipes[:5], many=True)
            return Response(serialized_recipes.data)
        else:
            return Response({})


class ReviewCreateView(CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        operation_summary="Create a review",
        operation_description="<b>You need to be authorized</b>\nCreate a review identified by dish_id",
        responses={
            201: ReviewSerializer(),
            400: "Bad Request"
        },
        tags=["Reviews"])
    def post(self, request, *args, **kwargs):
        dish_id = self.kwargs['dish_id']
        images = request.FILES.getlist('images')  # get a list of images from a request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=self.request.user, dish_id=dish_id)
            review = serializer.instance
            # save images and link them to the review
            for image in images:
                new_filename = handle_uploaded_file(image, image.name, "media/reviews/")  # change file name
                ReviewImages.objects.create(review=review, images=new_filename)
            dish = List_of_Dish.objects.get(id=dish_id)
            dish.update_rating()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a review",
        operation_description="<b>You need to be authorized</b>\nDelete a review identified by id",
        responses={
            204: "Successfully Delete review",
            404: "Not Found"
        },
        tags=["Reviews"])
    def delete(self, request, *args, **kwargs):
        review_id = self.kwargs['id']
        try:
            review = Reviews.objects.get(id=review_id)
        except Reviews.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user != review.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyCreateView(APIView):
    @swagger_auto_schema(
        request_body=ReviewSerializer,
        responses={status.HTTP_201_CREATED: ReviewSerializer()},
        operation_summary="Create reply to a review",
        operation_description="<b>You need to be authorized</b>\n"
                              "Create reply to a review identified by dish_id and parent_id",
        tags=["Reviews"])
    def post(self, request, dish_id, parent_id):
        try:
            # Get the dish object using the dish id
            dish = List_of_Dish.objects.get(id=dish_id)
        except List_of_Dish.DoesNotExist:
            return Response({'error': 'Dish not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Get the parent review object using the parent id and dish object
            parent_review = Reviews.objects.get(id=parent_id, dish=dish)
        except Reviews.DoesNotExist:
            return Response({'error': 'Parent review not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new review object with the dish, parent review, and author information
            serializer.save(dish=dish, parent=parent_review, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Like review",
        operation_description="<b>You need to be authorized</b>",
        responses={201: "success"},
        tags=["Reviews"])
    def post(self, request, review_id):
        review = get_object_or_404(Reviews, id=review_id)
        review.liked_by.add(request.user)
        review.save()
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Delete like from review",
        operation_description="<b>You need to be authorized</b>",
        responses={204: "success"},
        tags=["Reviews"])
    def delete(self, request, review_id):
        review = get_object_or_404(Reviews, id=review_id)
        review.liked_by.remove(request.user)
        review.save()
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data)


class CuisineCategoryPageView(APIView):
    @swagger_auto_schema(
        operation_summary="Get list of dishes filter by cuisine or category",
        operation_description="<b>Returns a paginated list of dishes. "
                              "The offset parameter specifies the number of dishes that already loaded. "
                              "It is needed for infinity scroll. "
                              "From number that in offset to offset + 9. "
                              "If the offset parameter is not specified, it defaults to 0.</b>",
        manual_parameters=[
            openapi.Parameter('offset', openapi.IN_QUERY, description="The number of dishes that need to upload.",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: List_of_Dish_Serializer(many=True)},
        tags=["Pages"])
    def get(self, request, **kwargs):
        offset = int(request.GET.get('offset', 0))  # if no request offset -> int(NoneType) so -> 0
        cuisine_id = kwargs.get('cuisine_id')
        category_id = kwargs.get('category_id')

        if cuisine_id:
            dishes = List_of_Dish.objects.filter(cuisine_id=cuisine_id)
        elif category_id:
            dishes = List_of_Dish.objects.filter(category_id=category_id)
        else:
            return Response({})

        if dishes.exists():
            serialized_recipes = List_of_Dish_Serializer(dishes[offset:offset + 9], many=True)
            return Response(serialized_recipes.data)
        else:
            return Response({})
