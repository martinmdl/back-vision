import pandas as pd

def cleanWeather(df_clima):   

    # Eliminar columnas innecesarias
    df_clima = df_clima.drop(columns=[
        "temp_source",
        "tmin_source",
        "tmax_source",
        "rhum_source",
        "prcp_source",
        "snwd",
        "snwd_source",
        "wspd_source",
        "pres_source",
        "cldc_source"
    ])

    # Transformar "year-month-date" en "fecha"
    df_clima["fecha"] = pd.to_datetime(df_clima[["year", "month", "day"]])
    df_clima = df_clima.drop(columns=["year", "month", "day"])
    df_clima = df_clima[["fecha", "temp", "tmin", "tmax", "rhum", "prcp", "wspd", "pres", "cldc"]]

    # Acotar periodo de tiempo
    # Inicio: 16/04/2025 - Fin: 04/09/2025
    ### TODO automatizar fechas ###
    df_clima = pd.DataFrame({ "fecha":pd.date_range(start="2025-04-16", end="2025-09-04") }).merge(df_clima, on="fecha", how="left")

    # Renombrar columnas
    df_clima = df_clima.rename(columns={
        "temp": "temp_avg",
        "tmin": "temp_min",
        "tmax": "temp_max",
        "rhum": "humedad",
        "prcp": "lluvia",
        "wspd": "viento",
        "pres": "presion",
        "cldc": "nubosidad"
    })

    ### TODO guardar df_clima en la base de datos ###
    ### TODO testear esta limpieza ###