import pandas as pd
import requests
from io import BytesIO
import gzip
from datetime import datetime

async def getWeather():

    anio = str(datetime.now().year)
    
    # Fetchear archivo
    weather_info = requests.get(f"https://data.meteostat.net/daily/{anio}/87585.csv.gz")
    if weather_info.status_code != 200:
        return {"error": "No se pudo descargar el archivo"}
    
    # Leer CSV comprimido directamente
    with gzip.open(BytesIO(weather_info.content), "rt") as f:
        df_clima = pd.read_csv(f)
    
    print(df_clima)

    