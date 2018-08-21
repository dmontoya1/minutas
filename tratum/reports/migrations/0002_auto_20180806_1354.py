# Generated by Django 2.0.6 on 2018-08-06 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20180803_1906'),
        ('document_manager', '0044_auto_20180726_1556'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BundleSaleSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Reporte de ventas de paquetes',
                'verbose_name_plural': 'Reportes de ventas de paquetes',
                'proxy': True,
                'indexes': [],
            },
            bases=('store.documentbundle',),
        ),
        migrations.CreateModel(
            name='CategorySaleSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Reporte de ventas documentos por categoría',
                'verbose_name_plural': 'Reportes de ventas documentos por categoría',
                'proxy': True,
                'indexes': [],
            },
            bases=('document_manager.category',),
        ),
        migrations.CreateModel(
            name='UserDocumentsSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Reporte de compras de documentos de clientes',
                'verbose_name_plural': 'Reportes de compras de documentos de clientes',
                'proxy': True,
                'indexes': [],
            },
            bases=('store.invoice',),
        ),
        migrations.AlterModelOptions(
            name='documentsalesummary',
            options={'verbose_name': 'Reporte de venta de documentos', 'verbose_name_plural': 'Reportes de venta de documentos'},
        ),
    ]