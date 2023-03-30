# Generated by Django 4.1.5 on 2023-03-05 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0013_rename_movie_reviews_dish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='email',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='name',
        ),
        migrations.AddField(
            model_name='reviews',
            name='author',
            field=models.ForeignKey(default=14, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviews',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='base.list_of_dish'),
        ),
    ]
