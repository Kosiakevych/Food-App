from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Avg
import math


class Instruction(models.Model):
    number = models.SmallIntegerField("Step")
    text = models.TextField("Instruction Text")

    def __str__(self):
        return f"{self.number}-{self.text}"


class Category(models.Model):
    name = models.CharField("Category Name", max_length=255)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField("Cuisine Name", max_length=255)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField("Ingredient Name", max_length=255)
    quantity = models.CharField("Quantity", max_length=255)
    unit = models.CharField("Unit", max_length=255)
    default_quant = models.SmallIntegerField("Default Quantity")

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"


class Equipment(models.Model):
    name = models.CharField("Equipment Name", max_length=255)

    def __str__(self):
        return self.name


# class Energy_value(models.Model):
#     def __str__(self):
#         return f"{self.calories} |{self.proteins} |{self.fats} |{self.carbohydrates}"


class Reviews(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    text = models.TextField("Message", max_length=5000)  # field for review text
    # user who created the review
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=14)
    # parent review (if it's a reply)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children")
    # the dish that the review belongs to
    dish = models.ForeignKey("List_of_Dish", on_delete=models.CASCADE, related_name='reviews')
    # rating for the dish
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_reviews")

    def __str__(self):
        return f"{self.author} - {self.dish} ({self.rating})"  # returns string representation of review

    def save(self, *args, **kwargs):
        if self.parent and self.parent.dish != self.dish:
            # raises an error if parent review dish does not match with the review dish
            raise ValueError("Parent review must be for the same dish.")
        super().save(*args, **kwargs)

    @property
    def is_reply(self):
        return self.parent is not None  # returns True if review is a reply


class ReviewImages(models.Model):
    review = models.ForeignKey(Reviews, related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='reviews/')


class List_of_Dish(models.Model):
    name = models.CharField("Name", max_length=255)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    description = models.TextField("Description", blank=True)
    time = models.CharField("Cooking_time", max_length=255)
    time_min = models.SmallIntegerField("Cooking time in min")
    url = models.SlugField(max_length=255)
    priority = models.SmallIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    instruction = models.ManyToManyField(Instruction, related_name="dish_instruction")
    ingredient = models.ManyToManyField(Ingredients, related_name="dish_ingredient")
    equipment = models.ManyToManyField(Equipment, related_name="dish_equipment")

    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    calories = models.SmallIntegerField("Calories", default=0, null=True)
    proteins = models.SmallIntegerField("Proteins", default=0, null=True)
    fats = models.SmallIntegerField("Fats", default=0, null=True)
    carbohydrates = models.SmallIntegerField("Carbohydrates", default=0, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='recipes_created'
    )

    def __str__(self):
        return self.name

    def update_rating(self):
        rating = Reviews.objects.filter(rating__isnull=False, dish=self).aggregate(Avg('rating'))['rating__avg']
        if rating:
            self.rating = math.ceil(rating * 2) / 2
        else:
            self.rating = None
        self.save()


class All_Ingredients(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.category}"
