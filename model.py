import joblib
import pandas as pd

# Cargar el modelo entrenado
model_path = "model/best_xgb_model.joblib"
model = joblib.load(model_path)

# Estados posibles
STATUS_GROUPS = ["functional", "functional needs repair", "non functional"]

def preprocess_inputs(input_df):
    """
    Preprocesa los datos para asegurar que coincidan con las columnas esperadas por el modelo.
    """
    model_features = model.get_booster().feature_names

    # Convertir `imputed_permit` a numérico
    if "imputed_permit" in input_df.columns:
        input_df["imputed_permit"] = input_df["imputed_permit"].map({True: 1, False: 0}).astype(int)

    # Convertir variables categóricas a dummies
    input_df = pd.get_dummies(input_df, drop_first=True)

    # Asegurar que las columnas del modelo estén presentes
    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0

    return input_df[model_features]

def predict_pump_status(input_df):
    """
    Predice el estado de las bombas usando el modelo entrenado.
    """
    processed_df = preprocess_inputs(input_df)
    probabilities = model.predict_proba(processed_df)

    predictions = [
        {
            "pump_id": str(input_df.iloc[idx]["id"]),  # Convertir a string para evitar problemas
            "status_group": STATUS_GROUPS[probs.argmax()],
            "probabilities": {STATUS_GROUPS[i]: float(prob) for i, prob in enumerate(probs)}  # Convertir a float nativo
        }
        for idx, probs in enumerate(probabilities)
    ]
    return predictions
