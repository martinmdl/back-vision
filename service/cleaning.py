import pandas as pd

def clean(xls_file):

    # DF_VENTA
    df_venta = pd.read_excel(xls_file, sheet_name="Ventas", skiprows=3) 
    
    columns_to_drop = ["Fecha", "Cerrada", "Caja", "Estado", "Cliente", "Mesa", "Sala", "Personas", 
                       "Camarero / Repartidor", "Medio de Pago", "Fiscal", "Comentario", "Origen", "Id. Origen"]
    
    df_venta = df_venta.drop(columns=columns_to_drop, errors='ignore')

    df_venta = df_venta.sort_values(by=["Id"]).reset_index(drop=True)

    df_venta["Creación"] = df_venta["Creación"].dt.strftime("%d/%m/%Y %H:%M:%S")

    df_venta["actualizacion"] = df_venta["Creación"]

    df_venta["activo"] = True

    df_venta = df_venta.rename(columns={
    "Id": "idVenta",
    "Creación": "creacion",
    "Total": "total",
    "Tipo de Venta": "tipo"
    })
    
    df_venta = df_venta[["idVenta", "total", "tipo", "creacion", "actualizacion", "activo"]]
    
    # DF_PRODUCTO
    df_producto = pd.read_excel(xls_file, sheet_name="Productos")

    # DF_DETALLE_VENTA
    df_detalle_venta = pd.read_excel(xls_file, sheet_name="Adiciones")

    return df_venta.head()
    
    