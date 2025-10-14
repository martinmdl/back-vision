import pandas as pd
import uuid
# import os

def clean_xls(xls_file):

    df_venta = pd.read_excel(xls_file, sheet_name="Ventas", skiprows=3)
    df_producto = pd.read_excel(xls_file, sheet_name="Productos")
    df_detalle_venta = pd.read_excel(xls_file, sheet_name="Adiciones")
    
    df_venta = clean_venta(df_venta)
    df_producto = clean_producto(df_producto)
    df_detalle_venta = clean_detalle_venta(df_detalle_venta, df_producto, df_venta)

    # print(df_detalle_venta.head(2))
    # print(df_venta.head(2))
    # print(df_producto.head(2))

    return df_venta, df_producto, df_detalle_venta

def clean_venta(df_venta):

    df_venta = df_venta.drop(columns=[
        "Fecha", "Cerrada", "Caja", "Estado", "Cliente", "Mesa", "Sala",
        "Personas", "Camarero / Repartidor", "Medio de Pago", "Fiscal", "Comentario", "Origen", "Id. Origen"
    ], errors='ignore')

    df_venta = df_venta.sort_values(by=["Id"]).reset_index(drop=True)

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
    
    return df_venta

def clean_producto(df_producto):

    # Elimina columna innecesarias
    df_producto = df_producto.drop(columns=[
        "Código", "Subcategoria", "Contiene modificadores",
        "Cant. en adiciones", "Cant. en modificadores"
    ], errors='ignore')

    # Crear idProducto con hashes
    df_producto["idProducto"] = df_producto.apply(
        lambda row: f"{row['Categoría'][:3].upper()}{str(uuid.uuid4())[:8]}", axis=1
    )

    df_producto["creacion"] = df_producto["actualizacion"] = pd.Timestamp.now().replace(microsecond=0)
    df_producto["activo"] = True

    # Renombrar columnas
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

    df_detalle_venta["Creación"] = pd.to_datetime(df_detalle_venta["Creación"])

    mapa = dict(zip(df_producto["nombre"], df_producto["idProducto"]))
    df_detalle_venta["idProducto"] = df_detalle_venta["Producto"].map(mapa)
    # Eliminar filas sin idProducto (productos no mapeados)
    df_detalle_venta = df_detalle_venta.dropna(subset=["idProducto"])
    df_detalle_venta = df_detalle_venta.drop(columns=["Producto", "Categoría"])
    df_detalle_venta = df_detalle_venta.reset_index(drop=True) # Reindexar despues de dropna 

    df_detalle_venta["Cancelada"] = df_detalle_venta["Cancelada"].map({"Si": True, "No": False})

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
        "Cantidad": "cantidad",
        "Cancelada": "cancelada",
        "Precio": "precio",
        "Costo base": "costo"
    })

    df_detalle_venta = df_detalle_venta[["idDetalle","idVenta","idProducto","cantidad","precio","costo","cancelada","creacion","actualizacion","activo"]]
    
    return df_detalle_venta

# # To test with local files
# file_path = os.path.join(os.path.dirname(__file__), "test_excel.xlsx")
# clean_xls(file_path)