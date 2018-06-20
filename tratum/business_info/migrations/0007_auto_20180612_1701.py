# Generated by Django 2.0.6 on 2018-06-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_info', '0006_siteconfig'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='siteconfig',
            options={'verbose_name': 'Configuración de sitio', 'verbose_name_plural': 'Configuración de sitio'},
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='about_page_image',
            field=models.ImageField(blank=True, null=True, upload_to='site/aboutus/', verbose_name='Imagen (Quienes sómos)'),
        ),
    ]