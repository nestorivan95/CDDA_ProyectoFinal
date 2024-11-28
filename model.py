import joblib
import pandas as pd

# Cargar el modelo entrenado
model = joblib.load("best_xgb_model.joblib")

# Estados posibles
STATUS_GROUPS = ["functional", "functional needs repair", "non functional"]

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
            input_df["imputed_permit"] = input_df["imputed_permit"].map({"True": 1, "False": 0, True: 1, False: 0})

        # Convertir todas las columnas categóricas a numéricas
        categorical_columns = [
            col for col in input_df.columns if input_df[col].dtype.name == "category"
        ]
        for col in categorical_columns:
            input_df[col] = input_df[col].cat.codes

        # Asegurar que las columnas del modelo estén presentes
        for col in model_features:
            if col not in input_df.columns:
                input_df[col] = 0  # Rellenar columnas faltantes con 0

        # Asegurar el orden de las columnas
        input_df = input_df[model_features]
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
