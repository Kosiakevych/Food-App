# Generated by Django 4.1.5 on 2023-03-07 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_reviewimages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewimages',
            old_name='image',
            new_name='images',
        ),
    ]