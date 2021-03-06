# Generated by Django 2.0.6 on 2018-06-28 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0028_auto_20180626_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFieldOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_manager.DocumentField', verbose_name='Campo')),
            ],
        ),
    ]
