# Generated by Django 2.0.6 on 2018-08-15 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20180815_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdocument',
            name='pdf_file',
            field=models.FileField(blank=True, editable=False, null=True, upload_to='pdfs'),
        ),
    ]
