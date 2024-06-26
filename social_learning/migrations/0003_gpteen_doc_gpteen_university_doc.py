# Generated by Django 4.2.6 on 2024-06-06 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_learning', '0002_quiz_quiz_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPTeen_doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('doc', models.FileField(upload_to='files/gpteen/')),
            ],
        ),
        migrations.CreateModel(
            name='GPTeen_University_doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(upload_to='files/university/')),
            ],
        ),
    ]
