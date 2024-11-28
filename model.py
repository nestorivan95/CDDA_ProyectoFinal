import joblib
import pandas as pd

# Cargar el modelo entrenado
model = joblib.load("best_xgb_model.joblib")
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.width', None)   

# Estados posibles
STATUS_GROUPS = ["functional", "functional needs repair", "non functional"]  

import pandas as pd

def preprocess_inputs(input_df):
    """
    Preprocesa los datos para asegurarse de que coincidan con las columnas esperadas por el modelo.
    
    Args:
        input_df (pd.DataFrame): Datos de entrada.
    
    Returns:
        pd.DataFrame: Datos procesados y alineados con el modelo.
    """
    try:
        # Obtener las columnas esperadas por el modelo
        model_features = model.get_booster().feature_names

        # Convertir `imputed_permit` a numérico (True -> 1, False -> 0)
        if "imputed_permit" in input_df.columns:
            input_df["imputed_permit"] = input_df["imputed_permit"].map({"True": 1, "False": 0, True: 1, False: 0}).astype(int)

        # Convertir las variables categóricas a variables dummy (como en el entrenamiento)
        categorical_columns = input_df.select_dtypes(include=['object']).columns
        input_df = pd.get_dummies(input_df, columns=categorical_columns, drop_first=True)

        # Asegurar que las columnas del modelo estén presentes
        for col in model_features:
            if col not in input_df.columns:
                input_df[col] = 0  # Rellenar columnas faltantes con 0

        # Asegurar el orden de las columnas
        input_df = input_df[model_features]

        # Imprimir el input_df procesado para depuración
        print("Input DataFrame después de preprocesamiento:")
        print(input_df.iloc[0].to_string())  # Imprime el primer registro procesado

        return input_df

    except Exception as e:
        raise ValueError(f"Error en el preprocesamiento de los datos: {e}")
    

def predict_pump_status(inputs):
    """
    Predice el estado de las bombas utilizando el modelo entrenado.
    
    Args:
        inputs (list of dict): Lista de registros con los datos requeridos para cada bomba.
    
    Returns:
        list of dict: Predicciones con las probabilidades para cada estado.
    """
    try:
        # Crear un DataFrame a partir de los inputs
        input_df = pd.DataFrame(inputs)

        # Guardar temporalmente los IDs (en una variable interna, no en los resultados)
        pump_ids = input_df["id"].tolist() if "id" in input_df.columns else [f"row_{idx}" for idx in range(len(input_df))]

        # Eliminar la columna `id` antes de la predicción (para evitar que el modelo la use)
        input_df = input_df.drop(columns=["id"], errors="ignore")

        # Preprocesar los datos antes de alimentar al modelo
        input_df = preprocess_inputs(input_df)

        # Realizar predicciones
        probabilities = model.predict_proba(input_df)

        # Construir los resultados
        predictions = [
            {
                "pump_id": pump_ids[idx],  # Usar el `id` original almacenado
                "probabilities": {
                    STATUS_GROUPS[i]: prob for i, prob in enumerate(probabilities[idx])
                }
            }
            for idx in range(len(pump_ids))
        ]

        return predictions
    except Exception as e:
        raise ValueError(f"Error en la predicción: {e}")

