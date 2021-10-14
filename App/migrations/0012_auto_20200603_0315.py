# Generated by Django 3.0.6 on 2020-06-03 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_auto_20200603_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='rubro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Rubros'),
        ),
        migrations.AlterField(
            model_name='det_venta',
            name='articulo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Articulos'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='articulo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.Articulos'),
        ),
    ]
