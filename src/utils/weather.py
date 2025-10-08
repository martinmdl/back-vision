import pandas as pd
import requests
from io import BytesIO
import gzip
from datetime import datetime

async def getWeather(df_venta):

    firstYear, lastYear = getYears(df_venta)

    # consultar ultimo año subido a la BD

    years = range(firstYear, lastYear + 1)
    df_list = []
    # EXCEL: 2020 - 2021 - 2022
    # EXCEL: 2020 - 2021 - 2022 - 2023 - 2024 - 2025
    #                       BD                   DF
    # 10/10/2022
    for year in years:
        # Fetch archivo.csv clima
        weather_info = requests.get(f"https://data.meteostat.net/daily/{year}/87585.csv.gz")
        if weather_info.status_code != 200:
            return {"error": f"No se pudo descargar el archivo para el año {year}"}
        # Leer CSV comprimido directamente
        with gzip.open(BytesIO(weather_info.content), "rt") as f:
            df_clima = pd.read_csv(f)
        df_list.append(df_clima)
    df_clima = pd.concat(df_list, ignore_index=True)
    
    return df_clima


def getYears(df_venta):

    firstYear = df_venta['creacion'].min().date().year
    lastYear = df_venta['creacion'].max().date().year

    return firstYear, lastYear