# Generated by Django 4.0 on 2021-12-16 10:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='valid_until',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
