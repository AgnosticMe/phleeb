# Generated by Django 3.1.5 on 2021-01-27 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_auto_20210126_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slider_blog',
            field=models.BooleanField(default=False),
        ),
    ]
