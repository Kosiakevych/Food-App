# Generated by Django 4.1.6 on 2023-02-18 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_list_of_dish_image_path720_alter_list_of_dish_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list_of_dish',
            old_name='image_path720',
            new_name='image720_path',
        ),
    ]
