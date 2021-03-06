# Generated by Django 2.0.6 on 2018-06-06 22:20

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0006_category_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='document_manager.Category', verbose_name='Categoría padre'),
        ),
        migrations.AlterField(
            model_name='category',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='¿Disponible para los usuarios?'),
        ),
        migrations.AlterField(
            model_name='document',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='document_manager.Category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='document',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='Contenido'),
        ),
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombre'),
        ),
    ]
