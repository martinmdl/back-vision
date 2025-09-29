import pandas as pd

def clean(xls_file):

    # file_path = os.path.join(os.path.dirname(__file__), "00_ventas.xls")
    # df_venta = pd.read_excel(file_path, sheet_name="Ventas", skiprows=3)
    # df_producto = pd.read_excel(file_path, sheet_name="Productos")
    # df_detalle_venta = pd.read_excel(file_path, sheet_name="Adiciones")

    df_venta = pd.read_excel(xls_file, sheet_name="Ventas", skiprows=3)
    df_venta = clean_venta(df_venta)
    
    df_producto = pd.read_excel(xls_file, sheet_name="Productos")
    df_producto = clean_producto(df_producto)

    df_detalle_venta = pd.read_excel(xls_file, sheet_name="Adiciones")
    df_detalle_venta = clean_detalle_venta(df_detalle_venta, df_producto, df_venta)

    return df_venta, df_producto, df_detalle_venta


def clean_venta(df_venta):

    df_venta = df_venta.drop(columns=[
        "Fecha", "Cerrada", "Caja", "Estado", "Cliente", "Mesa", "Sala",
        "Personas", "Camarero / Repartidor", "Medio de Pago", "Fiscal", "Comentario", "Origen", "Id. Origen"
    ], errors='ignore')

    df_venta = df_venta.sort_values(by=["Id"]).reset_index(drop=True)

    # Normalizar formato de fecha a datetime64[ns]
    df_venta["Creación"] = pd.to_datetime(df_venta["Creación"])

    df_venta["actualizacion"] = df_venta["Creación"]

    df_venta["activo"] = True

    df_venta = df_venta.rename(columns={
        "Id": "idVenta",
        "Creación": "creacion",
        "Total": "total",
        "Tipo de Venta": "tipo"
    })
    
    df_venta = df_venta[["idVenta", "total", "tipo", "creacion", "actualizacion", "activo"]]

    print(df_venta.head()) # borrar

    return df_venta

def clean_producto(df_producto):
    
    df_producto = df_producto.drop(columns=[
        "Código", "Subcategoria", "Contiene modificadores",
        "Cant. en adiciones", "Cant. en modificadores"
    ], errors='ignore')

    # Generar IDs de 3 cifras por cada productos dentro de una categoría
    df_producto["idProducto"] = (
        df_producto.groupby("Categoría").cumcount() + 1
    ).astype(str).str.zfill(3)

    # Generar prefijo en mayúscula con las primeras 3 letras de la categoría
    df_producto["idProducto"] = df_producto["Categoría"].str[:3].str.upper() + df_producto["idProducto"]

    df_producto["creacion"] = df_producto["actualizacion"] = pd.Timestamp.now().replace(microsecond=0)
    
    df_producto["activo"] = True

    df_producto = df_producto.rename(columns={
        "Nombre": "nombre",
        "Categoría": "categoria",
        "Cantidad": "cantidad",
        "Total ($)": "total_ARS"
    })

    df_producto = df_producto[["idProducto", "nombre", "categoria", "cantidad", "total_ARS", "creacion", "actualizacion", "activo"]]

    return df_producto

def clean_detalle_venta(df_detalle_venta, df_producto, df_venta):

    df_detalle_venta = df_detalle_venta.drop(columns=[
        "Costo modificadores", "Costo total", "Creada por", "Cocina",
        "Cancelada por", "Comentario", "Comentario de cancelación"
    ], errors='ignore')

    df_detalle_venta = df_detalle_venta.sort_values(by=["Id. Venta"]).reset_index(drop=True)

    df_detalle_venta["idDetalle"] = range(1, len(df_detalle_venta) + 1)
    
    # Normalizar formato de fecha a datetime64[ns]
    df_detalle_venta["Creación"] = pd.to_datetime(df_detalle_venta["Creación"])

    # Crear mapa de nombres a IDs
    mapa = dict(zip(df_producto["nombre"], df_producto["idProducto"]))

    # Reemplazar en detalle_venta
    df_detalle_venta["idProducto"] = df_detalle_venta["Producto"].map(mapa)

    # Eliminar columnas reemplazadas
    df_detalle_venta = df_detalle_venta.drop(columns=["Producto", "Categoría"])

    df_detalle_venta["Cancelada"] = df_detalle_venta["Cancelada"].map({"Si": True, "No": False})

    # Obtener fecha de creación desde df_venta
    df_detalle_venta_aux = df_detalle_venta.merge(
        df_venta[["idVenta", "creacion"]],
        left_on="Id. Venta",
        right_on="idVenta",
        how="left"
    )

    df_detalle_venta["creacion"] = df_detalle_venta["actualizacion"] = df_detalle_venta_aux["creacion"]

    df_detalle_venta["activo"] = True

    df_detalle_venta = df_detalle_venta.rename(columns={
        "Id. Venta": "idVenta",
        "Creación": "creacion",
        "Cantidad": "cantidad",
        "Cancelada": "cancelada",
        "Precio": "precio",
        "Costo base": "costo"
    })

    df_detalle_venta = df_detalle_venta[["idDetalle", "idVenta", "idProducto", "cantidad", "precio", "costo", "cancelada", "creacion", "actualizacion", "activo"]]

    return df_detalle_venta
    