# Generated by Django 4.1.5 on 2023-03-07 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_reviews_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='reviews/')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='base.reviews')),
            ],
        ),
    ]
