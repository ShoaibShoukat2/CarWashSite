# Generated by Django 5.0.4 on 2024-04-28 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_subscrationduration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('subscription_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.subscrationduration')),
                ('vehicle_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.vehicle')),
            ],
        ),
    ]
