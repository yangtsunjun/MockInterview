# Generated by Django 3.0.1 on 2020-08-26 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0027_remove_video_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='a1',
            field=models.TextField(blank=True),
        ),
    ]