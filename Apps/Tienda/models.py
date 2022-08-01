from django.db import models

# Create your models here.


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100, blank=False)
    precio = models.IntegerField(blank=False, null=False)
    descripcion = models.CharField(max_length=150, blank=True, null=True)


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True, unique=True, blank=False)
    nombre_usuario = models.CharField(max_length=200, blank=False)
    total = models.IntegerField(blank=False, null=False)
    fecha = models.DateField(auto_now=True)


class Inventario(models.Model):
    id_inventario = models.AutoField(
        primary_key=True, unique=True, blank=False)
    fk_id_producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, blank=False)
    cantidad = models.IntegerField(blank=False, null=False)
    estado = models.BooleanField(default=True, blank=False)


class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(
        primary_key=True, unique=True, blank=False)
    fk_id_venta = models.ForeignKey(
        Venta, on_delete=models.CASCADE, blank=False)
    fk_id_producto_detalle = models.ForeignKey(
        Producto, on_delete=models.CASCADE, blank=False)
    cantidad_comprada = models.IntegerField(blank=False, null=False)
    precio_cantidad_detalle = models.IntegerField(blank=False, null=False)


class CarritoCompra(models.Model):
    id_item_carrito = models.AutoField(
        primary_key=True, unique=True, blank=False)
    fk_id_producto_carrito = models.ForeignKey(
        Producto, on_delete=models.CASCADE, blank=False)
    cantidad_solicitada = models.IntegerField(blank=False, null=False)
    precio_cantidad_carrito = models.IntegerField(blank=False, null=False)
    estado_item = models.BooleanField(default=True, blank=False)
