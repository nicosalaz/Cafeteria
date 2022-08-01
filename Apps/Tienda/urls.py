from django.urls import path
from . import views

urlpatterns = [
    path('', views.Vista.index, name='index'),
    path('inventario/', views.Vista.inventario, name='inventario'),
    path('ventas/', views.Vista.ventas, name='ventas'),
    path('crearProducto/', views.ProductoController.crearProducto, name='crear'),
    path('editarProducto/<int:pk>/',
         views.Vista.editarProducto, name='editarProducto'),
    path('actualizarProducto/<int:pk>/',
         views.ProductoController.editarProducto, name='actualizarProducto'),
    path('eliminarProducto/<int:pk>/',
         views.InventarioController.eliminarProductoInventario, name='eliminar'),
    path('agregarProductoCarrito/<int:pk>/',
         views.CarritoController.agregarProductoCarrito),
    path('eliminarProductoCarrito/<int:pk>/',
         views.CarritoController.eliminarProductoCarrito, name='eliminarProductoCarrito'),
    path('agregarVenta/',
         views.VentaController.agregarVeta, name='agregarVenta'),
    path('detalleVenta/<int:pk>/',
         views.Vista.detalleVenta, name='detalleVenta'),

]
