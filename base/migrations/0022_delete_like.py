# Generated by Django 4.1.5 on 2023-03-08 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_reviews_liked_by_like'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]
