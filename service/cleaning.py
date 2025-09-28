import pandas as pd

def clean(xls_file):

    df_venta = pd.read_excel(xls_file, sheet_name="Ventas")
    df_producto = pd.read_excel(xls_file, sheet_name="Productos")
    df_detalle_venta = pd.read_excel(xls_file, sheet_name="Adiciones")

    # Limpieza de datos
    # TODO: Implementar la limpieza de datos según los requisitos