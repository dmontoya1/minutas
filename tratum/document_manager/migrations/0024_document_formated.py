# Generated by Django 2.0.6 on 2018-06-22 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0023_document_template_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='formated',
            field=models.BooleanField(default=False),
        ),
    ]