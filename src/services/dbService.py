from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from src.db.engine import engine

metadata = MetaData()

ventas = Table(
    "ventas", metadata,
    Column("idVenta", Integer, primary_key=True),
    Column("total", Float),
    Column("tipo", String),
    Column("creacion", TIMESTAMP),
    Column("actualizacion", TIMESTAMP),
    Column("activo", Boolean)
)

productos = Table(
    "productos", metadata,
    Column("idProducto", String, primary_key=True),
    Column("nombre", String),
    Column("categoria", String),
    Column("cantidad", Integer),
    Column("total_ARS", Float),
    Column("creacion", TIMESTAMP),
    Column("actualizacion", TIMESTAMP),
    Column("activo", Boolean)
)

detalle_ventas = Table(
    "detalle_ventas", metadata,
    Column("idDetalle", Integer, primary_key=True),
    Column("idVenta", Integer, ForeignKey("ventas.idVenta")),
    Column("idProducto", String, ForeignKey("productos.idProducto")),
    Column("cantidad", Integer),
    Column("precio", Float),
    Column("costo", Float),
    Column("cancelada", Boolean),
    Column("creacion", TIMESTAMP),
    Column("actualizacion", TIMESTAMP),
    Column("activo", Boolean)
)

# Crear tablas si no existen
metadata.create_all(engine)

def upsert_dataframe(df, table, pk_column):
    """Inserta o ignora registros existentes según pk_column"""
    with engine.begin() as conn:
        for row in df.to_dict(orient="records"):
            stmt = insert(table).values(**row).on_conflict_do_nothing(
                index_elements=[pk_column]
            )
            conn.execute(stmt)

def save_to_postgres(df_venta, df_producto, df_detalle_venta):
    upsert_dataframe(df_venta, ventas, "idVenta")
    upsert_dataframe(df_producto, productos, "idProducto")
    upsert_dataframe(df_detalle_venta, detalle_ventas, "idDetalle")
