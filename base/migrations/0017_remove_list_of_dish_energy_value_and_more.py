# Generated by Django 4.1.6 on 2023-03-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_list_of_dish_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list_of_dish',
            name='energy_value',
        ),
        migrations.AddField(
            model_name='list_of_dish',
            name='calories',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Calories'),
        ),
        migrations.AddField(
            model_name='list_of_dish',
            name='carbohydrates',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Carbohydrates'),
        ),
        migrations.AddField(
            model_name='list_of_dish',
            name='fats',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Fats'),
        ),
        migrations.AddField(
            model_name='list_of_dish',
            name='proteins',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Proteins'),
        ),
        migrations.DeleteModel(
            name='Energy_value',
        ),
    ]
