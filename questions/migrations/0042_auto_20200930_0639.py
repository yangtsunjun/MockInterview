# Generated by Django 3.1 on 2020-09-30 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0041_auto_20200927_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='q1',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q10',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q2',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q4',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q5',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q6',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q7',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q8',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='q9',
            field=models.TextField(blank=True),
        ),
    ]
