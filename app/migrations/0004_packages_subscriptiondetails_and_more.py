# Generated by Django 5.0.4 on 2024-04-27 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_car_image_remove_vehicle_user_car_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
                ('description', models.CharField(default='', max_length=200)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='package_type',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='subscription_duration',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='vehicle_name',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='car',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.car'),
        ),
        migrations.AlterField(
            model_name='car',
            name='file',
            field=models.FileField(default='', upload_to='car_files/'),
        ),
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='packages',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.packages'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='subscription_details',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.subscriptiondetails'),
        ),
        migrations.DeleteModel(
            name='PackageType',
        ),
        migrations.DeleteModel(
            name='SubscriptionDuration',
        ),
    ]
