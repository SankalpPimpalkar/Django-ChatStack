# Generated by Django 5.1.6 on 2025-02-13 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
