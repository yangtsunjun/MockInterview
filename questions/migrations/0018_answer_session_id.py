# Generated by Django 3.0.4 on 2020-07-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0017_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='session_id',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
