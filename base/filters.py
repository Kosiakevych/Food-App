from base.models import List_of_Dish

def filter_dish(request):
    # Get the list of equipment and ingredients from the request's query parameters
    equipment = set(request.query_params.getlist('equipment'))
    ingredient = set(request.query_params.getlist('ingredient'))
    # Get the minimum time for a dish to be prepared from the request's query parameters
    # If time_min parameter is not present, default it to 1440 minutes (1 day)
    time_min = request.query_params.get('time_min') or 1440

    # If both equipment and ingredient are not present, return False
    if not ingredient and not equipment:
        return False

    # Filter the list of dishes by the minimum time and prefetch related ingredients and equipment
    queryset = List_of_Dish.objects.filter(time_min__lte=int(time_min)).prefetch_related('ingredient', 'equipment')

    # Iterate over each dish in the filtered queryset
    for dish in queryset:
        # Check the missing ingredients and equipment for the dish
        missing_ingredient = set(ingr.name for ingr in dish.ingredient.all()) - ingredient
        missing_equipment = set(eq.name for eq in dish.equipment.all()) - equipment

        # Convert the missing ingredients and equipment to a list for easy display
        missing_ingredient_message = list(missing_ingredient) if missing_ingredient else None
        missing_equipment_message = list(missing_equipment) if missing_equipment else None

        # Calculate the priority of the dish based on the presence of ingredients and equipment
        priority = 0
        for ingr in dish.ingredient.all():
            if ingr.name in ingredient:
                priority += 100

        if equipment:
            for eq in dish.equipment.all():
                priority -= 100000
                if eq.name in equipment:
                    priority += 100000

        priority -= len(dish.ingredient.all())

        if priority / 100 == len(dish.ingredient.all()):
            priority += 10000

        # Set the calculated priority and missing ingredients and equipment message to the dish object
        dish.priority = priority
        dish.missing_ingredient_message = missing_ingredient_message
        dish.missing_equipment_message = missing_equipment_message

    # Sort the queryset based on the priority of the dishes in descending order
    queryset = sorted(queryset, key=lambda x: x.priority, reverse=True)

    return queryset
