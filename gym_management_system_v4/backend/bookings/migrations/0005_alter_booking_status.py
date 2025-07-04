# Generated by Django 3.2 on 2025-06-18 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_confirm_time_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(choices=[(0, '待确定'), (1, '已确定'), (2, '已完成')], default=0, verbose_name='预约状态'),
        ),
    ]
