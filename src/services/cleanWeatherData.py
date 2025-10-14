import pandas as pd
# import os

# def cleanWeather():

#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_dir, "test_clima.csv")
#     file_path = os.path.normpath(file_path)

#     df_clima = pd.read_csv(file_path)
#     df_clima_og = df_clima.copy()


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

## TESTING CON ARCHIVO LOCAL
## ALGUNAS FILAS QUEDAN CON NaN

    # return df_clima, df_clima_og

# df_clean, df_og = cleanWeather()

# print(df_og)
# print(df_clean)