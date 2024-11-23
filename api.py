from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Dummy Data for Prediction
STATUS_GROUPS = ["functional", "functional needs repair", "non functional"]

class WaterPumpInput(BaseModel):
    pump_ids: List[int]

class PredictionOutput(BaseModel):
    pump_id: int
    status_group: str

@app.post("/predict", response_model=List[PredictionOutput])
def predict(input_data: WaterPumpInput):
    """
    Dummy Prediction Logic: Assign a random status to each pump ID.
    """
    predictions = [
        {"pump_id": pump_id, "status_group": random.choice(STATUS_GROUPS)}
        for pump_id in input_data.pump_ids
    ]
    return predictions