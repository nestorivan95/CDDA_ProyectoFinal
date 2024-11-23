# Ciencia de Datos Aplicada: Proyecto Final

## Estado y Características de Bombas de Agua

Este proyecto es una aplicación interactiva que permite consultar el estado de una o varias bombas de agua, mostrar información detallada de las mismas y visualizar su ubicación en un mapa. Está construida usando *FastAPI* para el backend y *Streamlit* para la interfaz de usuario.

---

## *Características principales*

1. Consulta el estado de una o varias bombas de agua.
2. Visualiza la información geográfica y administrativa de cada bomba.
3. Muestra un mapa interactivo con los puntos de las bombas y su información en el tooltip.

---

## *Tecnologías utilizadas*

- *Python*: Lenguaje de programación principal.
- *FastAPI*: Framework utilizado para construir el API REST.
- *Streamlit*: Framework para construir la interfaz de usuario interactiva.
- *Folium*: Librería para mostrar mapas interactivos.
- *Pandas*: Para manipulación de datos del archivo CSV.
- *Streamlit-Folium*: Para integrar mapas interactivos en Streamlit.

---

## *Requisitos del sistema*

- *Python 3.8 o superior*
- *Pip* para manejar dependencias
- Sistema operativo: Windows, macOS o Linux

---

## *Estructura del proyecto*

```plaintext
├── app.py              # Código principal de la app en Streamlit
├── api.py              # Backend con FastAPI
├── model.py            # Simulación del modelo de predicción
├── data/
│   └── pumps_cleaned.csv # Datos de las bombas
├── requirements.txt    # Lista de dependencias
└── README.md           # Instrucciones del proyecto
```

---

## *Guía de instalación*

Sigue estos pasos para configurar el proyecto desde cero:

### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

# 2. Instalar las dependencias

Todas las dependencias están listadas en el archivo requirements.txt. Instalar con el siguiente comando:

```bash
pip install -r requirements.txt
```

# 3. Preparar los datos

Validar de que el archivo pumps_cleaned.csv esté en la carpeta data/. Este archivo contiene información sobre las bombas, excluyendo su estado (status_group).

# Cómo ejecutar el proyecto

# 1. Iniciar el backend (FastAPI)

Primero, se debe iniciar el servidor FastAPI para manejar las solicitudes REST:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

El servidor estará disponible en:

```bash
http://127.0.0.1:8000/docs
```

# 2. Iniciar la aplicación Streamlit

En una terminal separada, inicia la interfaz de usuario:

```bash
streamlit run app.py
```

Esto abrirá la aplicación en tu navegador, normalmente en:

```bash
http://localhost:8501
```


