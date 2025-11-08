from catboost import CatBoostRegressor
import requests
import pandas as pd
from ..db.managementDB import getDataForML

async def predecir_7_dias():

    model = CatBoostRegressor()
    model.load_model("src/model/catboost_model.cbm") # TODO: ver como cargar modelo fuera de la funcion

    df = getDataForML()
    productos = df["nombre"].unique()
    features = [
        "nombre", "temp_avg", "temp_min", "temp_max", "humedad", "lluvia", "viento", "presion", "nubosidad", "feriado", "tipo_feriado", "dia_semana", "mes"
    ]
    for i, f in enumerate(features):
        if i in model.get_cat_feature_indices():
            print(f"Categorical: {f}")
    df_clima = await obtener_clima_proximos_dias()
    df_clima["fecha"] = pd.to_datetime(df_clima["fecha"])
    predicciones = []

    for producto in productos:
        for _, clima_row in df_clima.iterrows():
            fila = {
                "nombre": producto,
                "temp_avg": clima_row["temp_avg"],
                "temp_min": clima_row["temp_min"],
                "temp_max": clima_row["temp_max"],
                "humedad": clima_row["humedad"],
                "lluvia": clima_row["lluvia"],
                "viento": clima_row["viento"],
                "presion": clima_row["presion"],
                "nubosidad": clima_row["nubosidad"],
                "tipo_feriado": 0, # TODO: hacer query a la BD para saber el tipo de feriado 
                "feriado": 0, # TODO: hacer query a la BD para saber si es feriado 
                "dia_semana": clima_row["fecha"].dayofweek,
                "mes": clima_row["fecha"].month
            }
            X_pred = pd.DataFrame([fila])[features]
            y_pred = model.predict(X_pred)[0]

            predicciones.append({
                "nombre": producto,
                "fecha_prediccion": clima_row["fecha"],
                "pred_cantidad": max(0, y_pred)  # Evita negativos
            })

    return pd.DataFrame(predicciones)

async def obtener_clima_proximos_dias():
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -34.593186,
        "longitude": -58.495826,
        "timezone": "auto",
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,relative_humidity_2m_mean,rain_sum,cloud_cover_mean,wind_speed_10m_mean,surface_pressure_mean",
        "forecast_days": 8
    }

    r = requests.get(base_url, params=params)
    r.raise_for_status()
    data = r.json()

    df_clima_futuro= pd.DataFrame({
        "fecha": data["daily"]["time"],
        "temp_avg": data["daily"]["temperature_2m_mean"],
        "temp_min": data["daily"]["temperature_2m_min"],
        "temp_max": data["daily"]["temperature_2m_max"],
        "humedad": data["daily"]["relative_humidity_2m_mean"],
        "lluvia": data["daily"]["rain_sum"],
        "viento": data["daily"]["wind_speed_10m_mean"],
        "presion": data["daily"]["surface_pressure_mean"],
        "nubosidad": data["daily"]["cloud_cover_mean"]
    })

    df_clima_futuro["fecha"] = pd.to_datetime(df_clima_futuro["fecha"])
    df_clima_futuro = df_clima_futuro.iloc[1:] 
    return df_clima_futuro