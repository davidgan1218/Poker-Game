# Generated by Django 3.2.7 on 2024-08-26 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20240826_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='deck',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
