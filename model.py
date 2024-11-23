import random

# Estados posibles
STATUS_GROUPS = ["functional", "functional needs repair", "non functional"]

def predict_pump_status(pump_ids):
    """
    Simula la predicción del estado de las bombas.
    Por ahora, devuelve un estado aleatorio para cada ID.
    """
    predictions = [
        {"pump_id": pump_id, "status_group": random.choice(STATUS_GROUPS)}
        for pump_id in pump_ids
    ]
    return predictions