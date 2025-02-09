# Generated by Django 5.0.4 on 2024-04-28 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_package_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='car_subscription',
        ),
        migrations.RemoveField(
            model_name='package',
            name='vehicle',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='file',
            field=models.FileField(default='', upload_to='vehicle_images/'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='name',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.CreateModel(
            name='SubscriptionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.CharField(choices=[('Annual', 'Annual Suscription'), ('6 Month', '6/Month Suscription'), ('Monthly', 'Monthly Suscription')], default='', max_length=10)),
                ('category', models.CharField(choices=[('Premium', 'Premium'), ('Special', 'Special')], default='', max_length=20)),
                ('vehicle_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subscriptiondata')),
            ],
        ),
        migrations.DeleteModel(
            name='CarSubscription',
        ),
        migrations.DeleteModel(
            name='Package',
        ),
    ]
