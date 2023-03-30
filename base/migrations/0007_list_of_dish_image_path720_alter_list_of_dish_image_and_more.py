# Generated by Django 4.1.6 on 2023-02-18 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_list_of_dish_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_of_dish',
            name='image_path720',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='list_of_dish',
            name='image',
            field=models.ImageField(upload_to='images/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='list_of_dish',
            name='image_path',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
