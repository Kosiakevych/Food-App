# Generated by Django 4.1.6 on 2023-02-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_list_of_dish_image'),
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
            field=models.ImageField(default='images/default.jpg', upload_to='media/images/'),
        ),
    ]
