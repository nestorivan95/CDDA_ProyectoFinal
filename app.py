import streamlit as st
import pandas as pd
from model import predict_pump_status

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
    "imputed_permit"
]

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
        input_data = [input_data]  # Convertir a lista para el modelo
        try:
            predictions = predict_pump_status(input_data)
            # Mostrar las predicciones de forma amigable
            for pred in predictions:
                pump_id = pred["pump_id"]
                st.write(f"### Predicciones para la bomba **{pump_id}**:")
                
                max_prob = max(pred['probabilities'], key=pred['probabilities'].get)
                max_prob_value = pred['probabilities'][max_prob]

                # Mostrar las probabilidades
                for status, prob in pred['probabilities'].items():
                    st.write(f"- **{status}:** {prob*100:.2f}%")

                # Establecer color según el estado
                if max_prob == "functional":
                    color = "green"
                    status_message = "Alta probabilidad de que esté **functional**."
                elif max_prob == "functional needs repair":
                    color = "yellow"
                    status_message = "Probabilidad media de que esté **functional needs repair**."
                else:
                    color = "red"
                    status_message = "Alta probabilidad de que esté **non functional**."

                # Mostrar el mensaje con el color adecuado
                st.markdown(f"<span style='color: {color};'>{status_message}</span>", unsafe_allow_html=True)
                st.write("---")
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
            st.error("Detalles técnicos:")
            st.error(str(e))

elif option == "Múltiples registros (archivo CSV)":
    st.subheader("Subir archivo CSV")
    uploaded_file = st.file_uploader("Cargue su archivo CSV", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        # Verificar si las columnas necesarias están presentes
        missing_columns = [col for col in columns if col not in data.columns]
        if missing_columns:
            st.error(f"El archivo no contiene las siguientes columnas requeridas: {missing_columns}")
        else:
            if st.button("Predecir"):
                try:
                    predictions = predict_pump_status(data.to_dict(orient="records"))
                    # Mostrar las predicciones de forma amigable
                    for pred in predictions:
                        pump_id = pred["pump_id"]
                        st.write(f"### Predicciones para la bomba **{pump_id}**:")
                        
                        max_prob = max(pred['probabilities'], key=pred['probabilities'].get)
                        max_prob_value = pred['probabilities'][max_prob]

                        # Mostrar las probabilidades
                        for status, prob in pred['probabilities'].items():
                            st.write(f"- **{status}:** {prob*100:.2f}%")
                        
                        # Establecer color según el estado
                        if max_prob == "functional":
                            color = "green"
                            status_message = "Alta probabilidad de que esté **functional**."
                        elif max_prob == "functional needs repair":
                            color = "yellow"
                            status_message = "Probabilidad media de que esté **functional needs repair**."
                        else:
                            color = "red"
                            status_message = "Alta probabilidad de que esté **non functional**."

                        # Mostrar el mensaje con el color adecuado
                        st.markdown(f"<span style='color: {color};'>{status_message}</span>", unsafe_allow_html=True)

                        st.write("---")
                except Exception as e:
                    st.error(f"Error en la predicción: {e}")
                    st.error("Detalles técnicos:")
                    st.error(str(e))
