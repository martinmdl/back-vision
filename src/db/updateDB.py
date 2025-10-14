from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import insert
from src.db.engine import engine
from enum import Enum

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

clima = Table(
    "clima", metadata,
    Column("fecha", TIMESTAMP, primary_key=True),
    Column("temp_avg", Float),
    Column("temp_min", Float),
    Column("temp_max", Float),
    Column("humedad", Float),
    Column("lluvia", Float),
    Column("viento", Float),
    Column("presion", Float),
    Column("nubosidad", Float)
)

class TableEnum(Enum):
    ventas = ("ventas", ventas)
    productos = ("productos", productos)
    detalle_ventas = ("detalle_ventas", detalle_ventas)
    clima = ("clima", clima)

    @classmethod
    def get_table(cls, name: str):
        for key, value in cls.__members__.items():
            if key.lower() == name.lower():
                return value.value[1]
        raise ValueError(f"Tabla '{name}' no encontrada.")

# Crear tablas si no existen
metadata.create_all(engine)

def save_to_postgres(df_table, table_name, id_table):
    table = TableEnum.get_table(table_name)
    upsert_dataframe(df_table, table, id_table)

def upsert_dataframe(df, table, pk_column):
    # Inserta o ignora registros existentes según pk_column
    with engine.begin() as begin:
        for row in df.to_dict(orient="records"):
            stmt = insert(table).values(**row).on_conflict_do_nothing(
                index_elements=[pk_column]
            )
            begin.execute(stmt)

def getDBLastYear():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT MAX(EXTRACT(YEAR FROM creacion)) FROM ventas"))
        last_year = result.scalar()
    return int(last_year) if last_year else None