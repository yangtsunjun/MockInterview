# Generated by Django 3.0.1 on 2020-07-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20200628_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment_Banking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=500, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='software_engineer',
            name='QuesNum',
            field=models.IntegerField(),
        ),
    ]