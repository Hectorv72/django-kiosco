# Generated by Django 3.0.6 on 2020-06-03 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_auto_20200603_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturas',
            name='detalle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Det_factura'),
        ),
    ]