# Generated by Django 2.0.6 on 2018-07-26 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0043_documentsection_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='documentsection',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
