# Generated by Django 5.0.4 on 2024-04-27 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_car_packagetype_subscriptionduration_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='image',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='user',
        ),
        migrations.AddField(
            model_name='car',
            name='file',
            field=models.FileField(default='default_file.txt', upload_to='car_files/'),
        ),
    ]
