# Generated by Django 4.1.6 on 2023-02-18 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_rename_image_path720_list_of_dish_image720_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list_of_dish',
            old_name='image720_path',
            new_name='image_path720',
        ),
    ]
