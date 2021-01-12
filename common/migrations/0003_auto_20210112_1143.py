# Generated by Django 3.1.4 on 2021-01-12 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20210111_0925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name_plural': 'images'},
        ),
        migrations.AlterField(
            model_name='itemimages',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='itemimages',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='common.item'),
        ),
    ]
