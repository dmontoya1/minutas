# Generated by Django 2.0.6 on 2018-07-19 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0039_auto_20180719_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL del video explicativo del documento'),
        ),
    ]
