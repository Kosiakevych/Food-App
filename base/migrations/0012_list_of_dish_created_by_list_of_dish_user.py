# Generated by Django 4.1.6 on 2023-03-04 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0011_alter_list_of_dish_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_of_dish',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='list_of_dish',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
