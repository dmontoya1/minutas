# Generated by Django 2.0.6 on 2018-06-12 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentbundle',
            name='documents',
            field=models.ManyToManyField(blank=True, to='document_manager.Document', verbose_name='Documentos'),
        ),
    ]
