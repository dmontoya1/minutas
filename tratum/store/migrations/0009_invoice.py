# Generated by Django 2.0.6 on 2018-08-01 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0008_documentbundle_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_discharged', models.BooleanField(default=False, verbose_name='¿Está pago?')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de pago')),
                ('payu_reference_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Referencia Pago payU')),
                ('payment_status', models.CharField(choices=[('AP', 'Aprobada'), ('PE', 'Pendiente'), ('CA', 'Cancelada'), ('RE', 'Rechazada')], default='PE', max_length=50, verbose_name='Estado del Pago')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Factura',
            },
        ),
    ]
