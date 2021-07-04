# Generated by Django 3.1.5 on 2021-01-31 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_blog_slider_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='popular',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
