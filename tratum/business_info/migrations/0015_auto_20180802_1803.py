# Generated by Django 2.0.6 on 2018-08-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_info', '0014_auto_20180802_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='about_page_image',
            field=models.ImageField(blank=True, help_text='La resolución requerida es de 800x1000px', null=True, upload_to='about-us', verbose_name='Imagen (Quienes somos)'),
        ),
    ]
