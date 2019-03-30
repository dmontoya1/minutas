# Generated by Django 2.0.9 on 2018-12-23 14:31

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20181027_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdocument',
            name='identifier',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, overwrite=True, populate_from=['document__name'], unique=True),
        ),
    ]