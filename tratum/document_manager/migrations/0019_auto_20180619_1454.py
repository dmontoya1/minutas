# Generated by Django 2.0.6 on 2018-06-19 19:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0018_auto_20180615_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenido'),
        ),
    ]
