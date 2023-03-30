from rest_framework import serializers

from accounts.models import FavoriteRecipe
from .models import List_of_Dish, Instruction, Ingredients, All_Ingredients, Equipment, Reviews, Cuisine, Category, \
    ReviewImages


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImages
        fields = ('images',)


class ReviewSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author.id')
    children = RecursiveSerializer(many=True, required=False)
    images = ReviewImageSerializer(many=True, read_only=True, required=False)
    liked_by_user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ('text', 'rating', 'author_id', "children", "images", "liked_by_user", "like_count", "is_author")

    def create(self, validated_data):
        images = validated_data.get('images')
        instance = self.Meta.model(**validated_data)
        instance.save()
        if images:
            for image in images:
                ReviewImages.objects.create(review=instance, images=image)
        return instance

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        return obj.liked_by.filter(id=user.id).exists()

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_is_author(self, obj):
        user = self.context['request'].user
        return obj.author == user if user.is_authenticated else False


class List_of_Dish_Serializer(serializers.ModelSerializer):
    ingredient_count = serializers.SerializerMethodField()
    portions = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    cuisine = serializers.SlugRelatedField(slug_field="name", read_only=True)
    missing_ingredient_message = serializers.CharField(read_only=True, allow_null=True)
    missing_equipment_message = serializers.CharField(read_only=True, allow_null=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = List_of_Dish
        fields = ("name", "category", "cuisine", "image", "url", "time", "rating", "ingredient_count", "portions",
                  'calories', 'proteins', 'fats', 'carbohydrates',
                  "missing_ingredient_message", "missing_equipment_message", "user_id", "is_favorite")

    def get_is_favorite(self, obj):
        user = self.context.get('request').user

        if user.is_authenticated:
            is_favorite = FavoriteRecipe.objects.filter(user=user, dish=obj).exists()
        else:
            is_favorite = False

        return is_favorite

    def get_ingredient_count(self, obj):
        return obj.ingredient.count()

    def get_portions(self, obj):
        return obj.ingredient.all()[0].default_quant

    def get_missing_ingredient_message(self, obj):
        ingredient = self.context.get("ingredient", [])
        missing_ingredient = [ingr.name for ingr in obj.ingredient.all() if ingr.name not in ingredient]

        messages = []

        if missing_ingredient:
            messages.append(f"Не хватает ингредиентов: {', '.join(missing_ingredient)}")

        if messages:
            return "; ".join(messages)
        else:
            return None

    def get_missing_equipment_message(self, obj):
        equipment = self.context.get("equipment", [])
        missing_equipment = [eq.name for eq in obj.equipment.all() if eq.name not in equipment]
        if missing_equipment:
            return f"Не хватает инструментов: {', '.join(missing_equipment)}"
        else:
            return None


# class EnergyValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Energy_value
#         fields = ('calories', 'proteins', 'fats', 'carbohydrates')


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ("text", "number")


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ("name", "quantity", "unit", "default_quant")


class Dish_Serializer(serializers.ModelSerializer):
    # energy_value = EnergyValueSerializer(read_only=True)
    instruction = InstructionSerializer(many=True, read_only=True)
    ingredient = IngredientsSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = List_of_Dish
        fields = (
            'name', 'image', 'ingredient', 'description', 'instruction', "time",
            'calories', 'proteins', 'fats', 'carbohydrates', "reviews")

    def get_reviews(self, obj):
        # Get all the top-level reviews for the given dish object
        reviews = Reviews.objects.filter(dish=obj, parent=None)
        return ReviewSerializer(reviews, many=True, context=self.context).data


class IngredientFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = All_Ingredients
        fields = ("name", "description", "image", "category")


class EquipmentFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("name",)


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ("name",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)
