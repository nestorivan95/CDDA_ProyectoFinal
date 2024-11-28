import streamlit as st
import pandas as pd
import requests
import json

# Dirección de la API
API_URL = "http://127.0.0.1:8000/predict"

# Configuración de Streamlit
st.title("Predicción del estado de las bombas de agua")

# Opciones iniciales
option = st.radio(
    "¿Cómo desea ingresar los datos?",
    ("Un solo registro", "Múltiples registros (archivo CSV)")
)

# Columnas necesarias
columns = [
    "id",
    "longitude",
    "latitude",
    "region",
    "extraction_type",
    "management",
    "payment_type",
    "quality_group",
    "quantity_group",
    "source",
    "waterpoint_type",
    "population_imputed",
    "altitud",
    "construction_year_imputed",
    "imputed_scheme__management",
    "imputed_permit",
]

# Función para mostrar resultados con formato mejorado
def display_results(predictions):
    for pred in predictions:
        pump_id = pred["pump_id"]
        status_group = pred["status_group"]
        probabilities = pred["probabilities"]
        
        # Mostrar el ID de la bomba
        st.subheader(f"Bomba ID: {pump_id}")

        # Mostrar probabilidades en formato de tabla
        prob_df = pd.DataFrame(list(probabilities.items()), columns=["Estado", "Probabilidad"])
        prob_df["Probabilidad"] = prob_df["Probabilidad"].apply(lambda x: f"{x * 100:.2f}%")
        st.write(prob_df)

        # Mostrar el estado predicho con color
        state_color = get_state_color(status_group)
        st.markdown(f"**Estado Predicho:** <span style='color:{state_color};'>{status_group}</span>", unsafe_allow_html=True)
        st.markdown("---")  # Línea divisoria

def get_state_color(status):
    """Devuelve el color correspondiente al estado predicho."""
    if status == "functional":
        return "green"
    elif status == "functional needs repair":
        return "yellow"
    elif status == "non functional":
        return "red"
    else:
        return "black"

if option == "Un solo registro":
    st.subheader("Ingresar un solo registro")

    # Crear inputs para cada columna
    input_data = {}
    for column in columns:
        if column == "id":
            input_data[column] = st.text_input(f"Ingrese {column}:")
        elif column in ["longitude", "latitude", "population_imputed", "altitud", "construction_year_imputed"]:
            input_data[column] = st.number_input(f"Ingrese {column}:", value=0.0)
        elif column == "imputed_permit":
            value = st.selectbox(f"Ingrese {column}:", ["True", "False"])
            input_data[column] = value
        else:
            input_data[column] = st.text_input(f"Ingrese {column}:")

    if st.button("Predecir"):
        try:
            response = requests.post(API_URL, json={"data": [input_data]})
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            predictions = response.json()

            # Mostrar resultados
            display_results(predictions)

        except requests.exceptions.RequestException as e:
            st.error(f"Error al conectar con la API: {e}")

elif option == "Múltiples registros (archivo CSV)":
    st.subheader("Subir archivo CSV")
    uploaded_file = st.file_uploader("Cargue su archivo CSV", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        if st.button("Predecir"):
            try:
                # Enviar los datos a la API
                response = requests.post(API_URL, json={"data": data.to_dict(orient="records")})
                response.raise_for_status()
                predictions = response.json()

                # Mostrar resultados
                display_results(predictions)

            except requests.exceptions.RequestException as e:
                st.error(f"Error al conectar con la API: {e}")
