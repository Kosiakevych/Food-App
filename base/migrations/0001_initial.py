# Generated by Django 4.1.5 on 2023-01-25 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Category Name')),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Cuisine Name')),
            ],
        ),
        migrations.CreateModel(
            name='Energy_value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calories', models.SmallIntegerField(verbose_name='Calories')),
                ('proteins', models.SmallIntegerField(verbose_name='Proteins')),
                ('fats', models.SmallIntegerField(verbose_name='Fats')),
                ('carbohydrates', models.SmallIntegerField(verbose_name='Carbohydrates')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Equipment Name')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Ingredient Name')),
                ('quantity', models.CharField(max_length=255, verbose_name='Quantity')),
                ('unit', models.CharField(max_length=255, verbose_name='Unit')),
                ('default_quant', models.SmallIntegerField(verbose_name='Default Quantity')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(verbose_name='Step')),
                ('text', models.TextField(verbose_name='Instruction Text')),
            ],
        ),
        migrations.CreateModel(
            name='List_of_Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('image', models.TextField(blank=True, verbose_name='Image')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('time', models.CharField(max_length=255, verbose_name='Cooking_time')),
                ('time_min', models.SmallIntegerField(verbose_name='Cooking time in min')),
                ('url', models.SlugField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.category')),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.cuisine')),
                ('energy_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.energy_value')),
                ('equipment', models.ManyToManyField(related_name='dish_equipment', to='base.equipment')),
                ('ingredient', models.ManyToManyField(related_name='dish_ingredient', to='base.ingredients')),
                ('instruction', models.ManyToManyField(related_name='dish_instruction', to='base.instruction')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='User name')),
                ('text', models.TextField(max_length=5000, verbose_name='Message')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.list_of_dish')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.reviews')),
            ],
        ),
    ]
