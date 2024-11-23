import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from model import predict_pump_status  # Importar la lógica del modelo

# Configuración inicial
DATA_PATH = "data/pumps_cleaned.csv"  # Ruta al archivo de datos

# Cargar datos
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    return data

pumps_data = load_data()

# Título de la aplicación
st.title("Estado y Características de Bombas de Agua")
st.markdown("Consulta la información de una o varias bombas de agua por sus IDs y visualiza sus características geográficas.")

# Entrada de datos
input_type = st.radio("Selecciona el tipo de entrada", ("Un solo ID", "Lista de IDs"))

if input_type == "Un solo ID":
    col1, col2 = st.columns([3, 1])  # Crear dos columnas para botones
    with col1:
        pump_id = st.number_input("Ingresa el ID de la bomba", min_value=1, step=1, key="pump_id")

    # Botón "Consultar" y "Limpiar búsqueda"
    with col2:
        if st.button("Limpiar búsqueda"):
            st.session_state.pop("pump_results", None)  # Limpiar resultados
            st.experimental_rerun()

    if st.button("Consultar"):
        with st.spinner("Procesando modelo..."):
            try:
                # Simular predicción con el modelo
                result = predict_pump_status([pump_id])
                st.session_state["pump_results"] = result
            except Exception as e:
                st.error(f"Error al procesar el modelo: {e}")

elif input_type == "Lista de IDs":
    col1, col2 = st.columns([3, 1])  # Crear dos columnas para botones
    with col1:
        pump_ids = st.text_area("Ingresa una lista de IDs separados por comas (ejemplo: 1,2,3)")

    with col2:
        if st.button("Limpiar búsqueda"):
            st.session_state.pop("pump_results", None)  # Limpiar resultados
            st.experimental_rerun()

    if st.button("Consultar"):
        with st.spinner("Procesando modelo..."):
            try:
                # Simular predicción con el modelo
                pump_ids_list = [int(x.strip()) for x in pump_ids.split(",") if x.strip().isdigit()]
                result = predict_pump_status(pump_ids_list)
                st.session_state["pump_results"] = result
            except Exception as e:
                st.error(f"Error al procesar el modelo: {e}")

# Mostrar resultados si existen en session_state
if "pump_results" in st.session_state:
    results = st.session_state["pump_results"]

    # Mostrar el estado de las bombas en lista
    st.markdown("### Estados de las Bombas")
    for result in results:
        state = result["status_group"]
        state_color = {
            "functional": "green",
            "functional needs repair": "yellow",
            "non functional": "red"
        }
        st.markdown(
            f"<div style='padding: 5px; background-color: {state_color[state]}; color: black; border-radius: 5px; font-weight: bold;'>"
            f"ID: {result['pump_id']} - Estado: {state}"
            f"</div>",
            unsafe_allow_html=True
        )

    # Mostrar el mapa con información en el tooltip
    st.markdown("### Ubicación Geográfica")
    map_object = folium.Map(location=[-6.369028, 34.888822], zoom_start=6)  # Coordenadas generales (Tanzania)

    for result in results:
        pump_info = pumps_data[pumps_data["id"] == result["pump_id"]]
        if not pump_info.empty:
            latitude = pump_info.iloc[0]["latitude"]
            longitude = pump_info.iloc[0]["longitude"]

            # Construir tooltip con información detallada
            tooltip_info = "<br>".join([
                f"<b>{column.capitalize().replace('_', ' ')}:</b> {value}"
                for column, value in pump_info.iloc[0].items()
                if column not in ["status_group", "id", "longitude", "latitude"]
            ])
            tooltip_info = f"<b>ID:</b> {result['pump_id']}<br>{tooltip_info}"  # Agregar ID al tooltip

            if pd.notna(latitude) and pd.notna(longitude):
                folium.Marker(
                    [latitude, longitude],
                    tooltip=tooltip_info,
                    popup=f"ID: {result['pump_id']} - Estado: {result['status_group']}"
                ).add_to(map_object)

    # Mostrar el mapa en Streamlit
    st_folium(map_object, width=800, height=600)