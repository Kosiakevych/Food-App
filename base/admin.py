from django.contrib import admin
from .models import Instruction, Category, Cuisine, List_of_Dish, Reviews, Equipment, Ingredients
from django.contrib import admin
from .forms import DishForm

# Register your models here.

admin.site.register(Instruction)
admin.site.register(Cuisine)
admin.site.register(Category)


class ListOfDishAdmin(admin.ModelAdmin):
    form = DishForm


admin.site.register(List_of_Dish, ListOfDishAdmin)
# admin.site.register(Energy_value)
admin.site.register(Reviews)
admin.site.register(Equipment)
admin.site.register(Ingredients)
