from ..db.managementDB import getDataForML
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np


# sobreescribir predictSales.pkl
def generateML():

    # fetch BD
    df = getDataForML()

    # Crear features de fecha
    df["creacion"] = pd.to_datetime(df["creacion"])
    df["dia_semana"] = df["creacion"].dt.dayofweek
    df["mes"] = df["creacion"].dt.month

    # Definir Target y Features
    y = df["cantidad_vendida"]
    X = df.drop(columns=["cantidad_vendida", "creacion"])

    # Columnas categóricas
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    # Train / test simple
    X_train = X[:-30] 
    X_test = X[-30:]
    y_train = y[:-30] 
    y_test = y[-30:]

    # Entrenar
    train_pool = Pool(X_train, y_train, cat_features=cat_cols)
    model = CatBoostRegressor(
    iterations=1000,
    depth=6,
    learning_rate=0.05,
    loss_function="RMSE",
    eval_metric="RMSE",
    random_seed=42,
    early_stopping_rounds=50,
    verbose=100
    )
    model.fit(train_pool)

    # Predecir y evaluar
    test_pool = Pool(X_test, cat_features=cat_cols)
    pred = model.predict(test_pool)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))

    print("Predicciones: ",pred)
    print("MAE: ", mae)
    print("RMSE: ", rmse)
    
    # Exportar modelo