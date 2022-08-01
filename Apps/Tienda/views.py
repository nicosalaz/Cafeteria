#from operator import index
#from re import template
from webbrowser import get
from django.shortcuts import render, redirect
from .models import CarritoCompra, DetalleVenta, Producto, Inventario, Venta
from django.db import transaction
from django.db.models import Sum
from datetime import datetime
#from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class Vista():

    def index(request):
        modelo = InventarioController()
        productos = modelo.desplegarInventario()
        carrito, total = CarritoController.desplegarCarrito()
        return render(request, 'index.html', {'productos': productos, 'carrito': carrito, 'total': total})

    def inventario(request):
        modelo = InventarioController()
        contexto = modelo.desplegarInventario()
        # modelo.desplegarInventario()
        return render(request, 'Inventario/inventarioProductos.html', {'productos': contexto})

    def ventas(request):
        ventas = VentaController.desplegarVentas()
        return render(request, 'Venta/ventas.html', {"ventas": ventas})

    def editarProducto(request, pk):
        contexto = ProductoController.getProducto(pk)
        return render(request, 'Producto/editarProducto.html', {"producto": contexto})

    def detalleVenta(request, pk):
        detalle = DetalleVentaController.desplegarDetalleVenta(pk)
        venta = VentaController.getVenta(pk)
        return render(request, 'DetalleVenta/detalleVenta.html', {'detalle': detalle, 'venta': venta})


class ProductoController():

    def crearProducto(request):
        objInventario = InventarioController()
        nombre_producto = request.POST.get('nombre_producto')
        precio_producto = request.POST.get('precio_producto')
        cantidad = request.POST.get('cantidad')
        desc = request.POST.get('descripcion')
        with transaction.atomic():
            query = Producto(nombre=nombre_producto,
                             precio=precio_producto,
                             descripcion=desc)
            query.save()
            last_id = Producto.objects.latest('id_producto')
            instanciaProducto = Producto.objects.get(
                id_producto=last_id.id_producto)
            objInventario.agregarAlInventario(instanciaProducto, cantidad)
        return redirect('inventario')

    def getProducto(pk):
        query = Inventario.objects.filter(
            fk_id_producto__exact=pk).select_related("fk_id_producto")
        for dato in query:
            data = {
                "id": dato.fk_id_producto.id_producto,
                "nombre": dato.fk_id_producto.nombre,
                "precio": dato.fk_id_producto.precio,
                "descripcion": dato.fk_id_producto.descripcion,
                "cantidad": dato.cantidad
            }
        return data

    def getInstanciaProducto(pk):
        return Producto.objects.get(id_producto__exact=pk)

    def editarProducto(request, pk):
        nombre_producto = request.POST.get('nombre_producto')
        precio_producto = request.POST.get('precio_producto')
        cantidad = request.POST.get('cantidad')
        desc = request.POST.get('descripcion')
        with transaction.atomic():
            Producto.objects.filter(id_producto__exact=pk).update(
                nombre=nombre_producto, precio=precio_producto, descripcion=desc)
            #producto.nombre = nombre_producto
            #producto.precio = precio_producto
            #producto.descripcion = desc
            InventarioController.editarInventario(
                identificador=pk, cantidad_producto=cantidad)
        return redirect('inventario')


class InventarioController():

    def desplegarInventario(self):
        query = Inventario.objects.select_related(
            'fk_id_producto').filter(cantidad__gt=0, estado__exact=True)
        return query

    def agregarAlInventario(self, identificador, cantidad_producto):
        query = Inventario(fk_id_producto=identificador,
                           cantidad=cantidad_producto)
        query.save()

    def editarInventario(identificador, cantidad_producto):
        Inventario.objects.filter(fk_id_producto__exact=identificador).update(
            cantidad=cantidad_producto)

    def eliminarProductoInventario(request, pk):
        Inventario.objects.filter(
            fk_id_producto__exact=pk).update(estado=False)
        return redirect('inventario')

    def restarInventario(self, pk, cantidadLlevada):
        saldoActual = Inventario.objects.get(fk_id_producto__exact=pk)
        nuevoSaldo = saldoActual.cantidad - cantidadLlevada
        Inventario.objects.filter(
            fk_id_producto__exact=pk).update(cantidad=nuevoSaldo)

    """
    SELECT tp.id_producto,tp.nombre,tp.precio,tp.descripcion,ti.cantidad
    FROM "Tienda_inventario" as ti 
    inner JOIN "Tienda_producto" as tp on(tp.id_producto = ti.fk_id_producto_id)
    
     @csrf_exempt
    def get_producto(request, pk, *args, **kwargs):
        if request.method == 'GET':
            data = {
                'id_producto': pk
            }
            query = Inventario.objects.filter(fk_id_producto__exact=pk)
            print(query)
            return HttpResponse(query)
    """


class VentaController():
    def desplegarVentas():
        query = Venta.objects.all()
        return query

    def agregarVeta(requet):
        objDetalle = DetalleVentaController()
        objCarrito = CarritoController()
        objInvantario = InventarioController()
        nombre_comprador = requet.POST.get('nombre_cliente')
        info_carrito = CarritoController.getItemsCarritoCompra()
        with transaction.atomic():
            try:
                Venta.objects.create(
                    nombre_usuario=nombre_comprador,
                    total=info_carrito['total']['precio_cantidad_carrito__sum'],
                    fecha=datetime.today().strftime('%Y-%m-%d'))
                last_id = Venta.objects.latest('id_venta')
                instanciaVenta = Venta.objects.get(
                    id_venta=last_id.id_venta)
                for dato in info_carrito['items']:
                    objDetalle.agregarDetalle(
                        dato.cantidad_solicitada, dato.precio_cantidad_carrito,
                        dato.fk_id_producto_carrito, instanciaVenta)
                    objCarrito.setEstadoItem(dato.id_item_carrito)
                    objInvantario.restarInventario(
                        dato.fk_id_producto_carrito, dato.cantidad_solicitada)
            except Exception as e:
                print(e)
                transaction.rollback()
        return redirect('index')

    def getVenta(pk):
        return Venta.objects.get(id_venta__exact=pk)


class CarritoController():
    def agregarProductoCarrito(request, pk):
        existeProducto = CarritoCompra.objects.filter(
            fk_id_producto_carrito__exact=pk, estado_item__exact=True)
        cantidadDeseada = request.POST.get('cantidadDeseada')
        if existeProducto:
            print(existeProducto)
        else:
            prod = ProductoController.getProducto(pk)
            instanciaProd = ProductoController.getInstanciaProducto(pk)
            precio_cantidad = int(prod['precio'])*int(cantidadDeseada)
            CarritoCompra.objects.create(
                cantidad_solicitada=cantidadDeseada,
                precio_cantidad_carrito=precio_cantidad,
                fk_id_producto_carrito=instanciaProd)

        return redirect('index')

    def desplegarCarrito():
        query = CarritoCompra.objects.select_related(
            "fk_id_producto_carrito").filter(estado_item__exact=True)
        total = CarritoCompra.objects.filter(estado_item__exact=True).aggregate(
            Sum('precio_cantidad_carrito'))
        return query, total

    def eliminarProductoCarrito(request, pk):
        CarritoCompra.objects.filter(
            id_item_carrito__exact=pk).update(estado_item=False)
        return redirect("index")

    def getItemsCarritoCompra():
        query = CarritoCompra.objects.filter(estado_item__exact=True)
        total = CarritoCompra.objects.filter(estado_item__exact=True).aggregate(
            Sum('precio_cantidad_carrito'))
        data = {
            'items': query,
            'total': total
        }
        return data

    def setEstadoItem(self, pk):
        CarritoCompra.objects.filter(
            id_item_carrito__exact=pk).update(estado_item=False)


class DetalleVentaController():
    def agregarDetalle(self, cantidad_prod, precio, instanciaProd, instanciaVenta):
        DetalleVenta.objects.create(cantidad_comprada=cantidad_prod,
                                    precio_cantidad_detalle=precio,
                                    fk_id_producto_detalle=instanciaProd,
                                    fk_id_venta=instanciaVenta)

    def desplegarDetalleVenta(pk):
        return DetalleVenta.objects.filter(fk_id_venta__exact=pk).select_related(
            'fk_id_venta').select_related(
            'fk_id_producto_detalle')
