# Generated by Django 2.0.6 on 2018-09-24 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_info', '0017_auto_20180906_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slideritem',
            name='image',
            field=models.ImageField(help_text='La resolución es 1920 x 1080p', upload_to='slides', verbose_name='Imagen'),
        ),
    ]