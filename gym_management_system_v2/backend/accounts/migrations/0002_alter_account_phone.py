# Generated by Django 4.2 on 2025-06-17 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='手机号'),
        ),
    ]
