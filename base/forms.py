from django import forms
from .models import List_of_Dish, Instruction, Ingredients


class DishForm(forms.ModelForm):
    class Meta:
        model = List_of_Dish
        fields = ['name', 'image', 'description', 'time', 'time_min', 'url', 'instruction', 'ingredient', 'equipment',
                  'cuisine', "calories", "proteins", 'fats', 'carbohydrates', 'category']

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        self.fields['instruction'].queryset = Instruction.objects.filter(dish_instruction=self.instance)
        self.fields['ingredient'].queryset = Ingredients.objects.filter(dish_ingredient=self.instance)
