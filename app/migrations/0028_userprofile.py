# Generated by Django 5.0.4 on 2024-05-09 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=100)),
                ('subscription', models.CharField(blank=True, max_length=100, null=True)),
                ('package', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.signup')),
            ],
        ),
    ]
