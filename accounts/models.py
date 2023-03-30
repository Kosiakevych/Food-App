from django.db import models
from django.contrib.auth.models import User, AbstractUser

from base.models import List_of_Dish


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    email = models.EmailField(max_length=100)
    is_email_verified = models.BooleanField(default=False)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(List_of_Dish, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'dish']