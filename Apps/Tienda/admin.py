from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Inventario)
admin.site.register(CarritoCompra)
admin.site.register(DetalleVenta)