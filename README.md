# Ciencia de Datos Aplicada: Proyecto Final

## Integrantes: 
- Santiago Najar Gomez
- Juan Diego Velásquez
- Carlos Alberto Niño Ramirez
- Nestor Ivan Ramirez

## Estado y Características de Bombas de Agua

Este proyecto es una aplicación interactiva que permite consultar el estado de una o varias bombas de agua, mostrar información detallada de las mismas y visualizar su ubicación en un mapa. Está construida usando *FastAPI* para el backend, *Streamlit* para la interfaz de usuario, y *Dash* para visualizaciones interactivas adicionales.

---

## *Características principales*

1. Consulta el estado de una o varias bombas de agua.
2. Visualiza la información geográfica y administrativa de cada bomba.
3. Muestra un mapa interactivo con los puntos de las bombas y su información en el tooltip.
4. Dashboard interactivo con gráficas y filtros dinámicos, desarrollado con *Dash*.

---

## *Tecnologías utilizadas*

- *Python*: Lenguaje de programación principal.
- *FastAPI*: Framework utilizado para construir el API REST.
- *Streamlit*: Framework para construir la interfaz de usuario interactiva.
- *Dash*: Framework para el desarrollo de un dashboard interactivo.
- *Folium*: Librería para mostrar mapas interactivos.
- *Pandas*: Para manipulación de datos del archivo CSV.
- *Streamlit-Folium*: Para integrar mapas interactivos en Streamlit.
- *Plotly*: Para visualización interactiva de los datos.

---

## *Requisitos del sistema*

- *Python 3.8 o superior*
- *Pip* para manejar dependencias
- Sistema operativo: Windows, macOS o Linux

---

## *Estructura del proyecto*

```bash
├── app.py              # Código principal de la app en Streamlit
├── api.py              # Backend con FastAPI
├── model.py            # Simulación del modelo de predicción
├── modeldash.py        # Lógica para manejar los datos y filtros de Dash
├── dash.py             # Framework para desarrollar el dashboard con Dash
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

### 2. Instalar las dependencias

Todas las dependencias están listadas en el archivo requirements.txt. Instalar con el siguiente comando:

```bash
pip install -r requirements.txt
```

### 3. Preparar los datos

Validar de que el archivo pumps_cleaned.csv esté en la carpeta data/. Este archivo contiene información sobre las bombas, excluyendo su estado (status_group).

## *Cómo ejecutar el proyecto*

### 1. Iniciar el backend (FastAPI)

Primero, se debe iniciar el servidor FastAPI para manejar las solicitudes REST:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

El servidor estará disponible en: **http://127.0.0.1:8000/docs**


### 2. Iniciar la aplicación Streamlit

En una terminal separada, inicia la interfaz de usuario:

```bash
streamlit run app.py
```

Esto abrirá la aplicación en tu navegador, normalmente en: http://localhost:8501

### 3. Iniciar Dashboard

Para iniciar el dashboard interactivo desarrollado con Dash, sigue estos pasos:

En una terminal separada, navega al directorio del proyecto y ejecuta el siguiente comando para iniciar el servidor de Dash:


```bash
python dash.py
```

Esto lanzará el servidor Dash en el puerto 8050. La aplicación estará disponible en:

```bash
http://127.0.0.1:8050

```

## Estructura Dash

- modeldash.py: Este archivo contiene la lógica encargada de manejar los datos y la lógica de los filtros para el dashboard. Es donde se definen las funciones que controlan la manipulación de datos y los cálculos necesarios para actualizar las visualizaciones.

- dash.py: Aquí se encuentra el desarrollo del framework Dash. En este archivo, se configura la aplicación Dash, se definen los elementos del layout (gráficos, filtros, etc.) y se enlazan los callbacks para actualizar los componentes según las selecciones del usuario.

## Conclusiones

- Se obtuvo un producto de datos cuyo modelo, con una precisión del 84%, representa una herramienta importante para la optimización de recursos por parte de las entidades gubernamentales de Tanzania.
- El proceso de limpieza e imputación de los datos faltantes fue el proceso más arduo, ya que el Gobierno de Tanzania tiene poca información disponible y, además, se presentaban muchos valores erróneos.
- Se espera que con el uso de la herramienta el número de pozos reparados al mes aumente ya que se dispondrá de mejor forma los recursos disponibles para mantenimiento.
- Para obtener un modelo con mejores resultados sería ideal contar con datos actualizados, valores categóricos bien definidos y valores balanceados geográficamente. Igualmente pueden existir variables adicionales que aporten al modelo como comportamientos sociales o climáticos.
- Durante el proceso, dedicamos una buena cantidad de tiempo al Análisis Exploratorio de Datos (EDA) y elaboramos informes de calidad de datos que nos permitieron obtener perspectivas esenciales sobre la información.
- Es importante no descartar de inmediato las características con alta cardinalidad; en su lugar, agrupamos las clases raras en una nueva clase única, lo que facilitó un análisis más consistente y manejable.


