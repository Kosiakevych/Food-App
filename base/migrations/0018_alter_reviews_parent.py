# Generated by Django 4.1.5 on 2023-03-07 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_remove_list_of_dish_energy_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='base.reviews'),
        ),
    ]
