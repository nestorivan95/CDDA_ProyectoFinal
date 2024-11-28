from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from model import predict_pump_status

app = FastAPI()

# Clase para validar la entrada
class PumpRecord(BaseModel):
    id: str
    longitude: float
    latitude: float
    region: str
    extraction_type: str
    management: str
    payment_type: str
    quality_group: str
    quantity_group: str
    source: str
    waterpoint_type: str
    population_imputed: int
    altitud: float
    construction_year_imputed: int
    imputed_scheme__management: str
    imputed_permit: bool

class PumpData(BaseModel):
    data: List[PumpRecord]

@app.post("/predict")
def predict(data: PumpData):
    try:
        input_df = pd.DataFrame([record.dict() for record in data.data])
        predictions = predict_pump_status(input_df)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")
