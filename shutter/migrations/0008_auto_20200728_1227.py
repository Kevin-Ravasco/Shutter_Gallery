# Generated by Django 3.0.8 on 2020-07-28 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutter', '0007_auto_20200728_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
