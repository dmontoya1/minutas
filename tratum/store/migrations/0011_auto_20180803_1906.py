# Generated by Django 2.0.6 on 2018-08-04 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0044_auto_20180726_1556'),
        ('store', '0010_merge_20180801_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='document_manager.Document', verbose_name='Documento'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.DocumentBundle', verbose_name='Paquete'),
        ),
    ]
