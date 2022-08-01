function botonEliminar(x) {
    id_producto = x.value;
    formDelete = document.getElementById("formDelete").action="/Tienda/eliminarProducto/"+id_producto+"/";
    textmodal = document.getElementById("modelTextEdit").innerHTML="<h6>¿Desea eliminar este producto?</h6>"
}

function eliminarProducto() {
    document.getElementById("formDelete").submit();
}

function agregarCarrito(x) {
    id_prod = x.id;
    formulario = document.getElementById('form-carrito');
    formulario.action='/Tienda/agregarProductoCarrito/'+id_prod+'/';
    document.getElementById('cantidadDeseada').max=x.value;
}