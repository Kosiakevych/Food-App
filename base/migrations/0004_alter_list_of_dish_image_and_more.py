# Generated by Django 4.1.6 on 2023-02-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_list_of_dish_image_path_alter_list_of_dish_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_of_dish',
            name='image',
            field=models.ImageField(upload_to='media/images/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='list_of_dish',
            name='image_path',
            field=models.ImageField(default='images/default.jpg', max_length=255, upload_to='media/images/'),
        ),
    ]
