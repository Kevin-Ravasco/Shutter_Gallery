# Generated by Django 3.0.8 on 2020-07-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutter', '0009_auto_20200728_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/profiles/defaut_user.png', upload_to='profiles'),
        ),
    ]
