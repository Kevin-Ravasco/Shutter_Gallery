# Generated by Django 3.0.8 on 2020-07-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutter', '0010_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/profiles/default_user.png', upload_to='profiles'),
        ),
    ]