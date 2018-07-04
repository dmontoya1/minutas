# Generated by Django 2.0.6 on 2018-07-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_info', '0008_slideritem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfig',
            name='about_page_image',
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='facebook_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL Facebook (landing)'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='instagram_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL Instagram (landing)'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='landing_contact',
            field=models.TextField(blank=True, null=True, verbose_name='Correo de contacto (landing)'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='landing_phone',
            field=models.TextField(blank=True, null=True, verbose_name='Teléfono de contacto (landing)'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='twitter_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL Twitter (landing)'),
        ),
    ]
