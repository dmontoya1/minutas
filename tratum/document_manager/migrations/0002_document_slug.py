# Generated by Django 2.0.6 on 2018-06-01 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
