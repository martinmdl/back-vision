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

    return df_clima