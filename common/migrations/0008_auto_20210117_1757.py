# Generated by Django 3.1.4 on 2021-01-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20210117_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(choices=[('R', 'RAW')], max_length=100),
        ),
    ]
