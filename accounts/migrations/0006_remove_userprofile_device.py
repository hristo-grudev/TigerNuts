# Generated by Django 3.1.4 on 2021-01-17 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210117_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='device',
        ),
    ]
