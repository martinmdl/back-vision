unifyDataFrameQuery = """
    WITH fechas AS (
        SELECT DISTINCT creacion
        FROM detalle_ventas
    ),
    feriados AS (
        SELECT DISTINCT 
            f.fecha,
            tf.tipo,
            f.nombre
        FROM feriado f
        INNER JOIN tipo_feriado tf ON tf.id_tipo_feriado = f.tipo
    )
    SELECT
        p.id_producto,
        p.nombre,
        f.creacion,
        COALESCE(SUM(dv.cantidad), 0) AS cantidad_vendida,
        c.temp_avg,
        c.temp_min,
        c.temp_max,
        c.humedad,
        c.lluvia,
        c.viento,
        c.presion,
        c.nubosidad,
        COALESCE(fer.tipo, '-') AS tipo_feriado,
        COALESCE(fer.nombre, '-') AS feriado
    FROM productos p
    CROSS JOIN fechas f
    LEFT JOIN detalle_ventas dv 
    ON dv.id_producto = p.id_producto 
    AND dv.creacion = f.creacion
    LEFT JOIN clima c
    ON c.fecha = f.creacion
    LEFT JOIN feriados fer ON fer.fecha = f.creacion
    GROUP BY p.id_producto, p.nombre, f.creacion, c.temp_avg, c.temp_min, c.temp_max, 
    c.humedad, c.lluvia, c.viento, c.presion, c.nubosidad, fer.tipo, fer.nombre
    ORDER BY f.creacion, p.nombre;
"""

getDBLastYearQuery = "SELECT MAX(EXTRACT(YEAR FROM creacion)) FROM ventas"