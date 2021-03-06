# Generated by Django 3.0.5 on 2020-07-19 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0020_merge_20200718_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data_Scientist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Database_Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Network_Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quantitative_Trading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sales_Trading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='System_Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venture_Capital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuesNum', models.IntegerField()),
                ('Difficulties', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=100)),
                ('Ques', models.TextField(max_length=500)),
                ('Ans', models.TextField(max_length=800, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='investment_banking',
            name='Ans',
            field=models.TextField(max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='software_engineer',
            name='Ans',
            field=models.TextField(max_length=800, null=True),
        ),
    ]
