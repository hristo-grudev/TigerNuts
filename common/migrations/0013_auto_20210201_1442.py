# Generated by Django 3.1.4 on 2021-02-01 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_auto_20210131_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='being_delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
    ]
