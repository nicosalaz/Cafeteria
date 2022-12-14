# Generated by Django 4.0.6 on 2022-07-29 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.IntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id_venta', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre_usuario', models.CharField(max_length=200)),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cantidad', models.IntegerField()),
                ('fk_id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id_detalle_venta', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cantidad_comprada', models.IntegerField()),
                ('precio_cantidad_detalle', models.IntegerField()),
                ('fk_id_producto_detalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tienda.producto')),
                ('fk_id_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tienda.venta')),
            ],
        ),
        migrations.CreateModel(
            name='CarritoCompra',
            fields=[
                ('id_item_carrito', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cantidad_solicitada', models.IntegerField()),
                ('precio_cantidad_carrito', models.IntegerField()),
                ('estado_item', models.BooleanField(default=True)),
                ('fk_id_producto_carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tienda.producto')),
            ],
        ),
    ]
