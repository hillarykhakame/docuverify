# Generated by Django 5.1 on 2024-08-23 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_documentverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
