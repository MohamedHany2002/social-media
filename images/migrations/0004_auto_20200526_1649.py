# Generated by Django 3.0.2 on 2020-05-26 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0003_image_post_likes_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.AlterField(
            model_name='image_post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes_images', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.person')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='persons',
            field=models.ManyToManyField(related_name='groups', through='images.member', to='images.person'),
        ),
    ]
