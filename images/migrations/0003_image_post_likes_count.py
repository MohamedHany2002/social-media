# Generated by Django 2.2.7 on 2020-03-21 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20200307_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='image_post',
            name='likes_count',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
