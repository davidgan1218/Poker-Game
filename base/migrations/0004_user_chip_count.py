# Generated by Django 3.2.7 on 2024-08-26 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chip_count',
            field=models.IntegerField(default=5000),
        ),
    ]
