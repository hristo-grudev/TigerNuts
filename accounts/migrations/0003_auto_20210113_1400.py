# Generated by Django 3.1.4 on 2021-01-13 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210112_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='images/Anonymous-Avatar.png', upload_to='profiles/'),
        ),
    ]
