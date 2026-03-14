import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os

# Configuración de página
st.set_page_config(page_title="COVID-19 Perú Analysis", layout="wide")

# --- CARGA DE DATOS ---
@st.cache_data
def get_data():
    path = kagglehub.dataset_download("martinclark/peru-covid19-august-2020")
    csv_file = [f for f in os.listdir(path) if f.endswith('.csv')][0]
    return pd.read_csv(os.path.join(path, csv_file))

df = get_data()
if 'FECHA_RESULTADO' in df.columns:
    df['FECHA_RESULTADO'] = pd.to_datetime(df['FECHA_RESULTADO'])

# --- NAVEGACIÓN ---
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Página de Inicio", "Panel de Análisis"])

# --- PÁGINA DE INICIO (LANDING) ---
if page == "Página de Inicio":
    st.title("🦠 Análisis COVID-19: Perú 2020")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Bienvenido al Panel Integrador
        Este proyecto utiliza el dataset oficial de casos positivos en Perú para realizar un análisis descriptivo. 
        Como experto en datos, hemos estructurado esta herramienta para entender:
        * **Impacto por Región:** Identificación de focos críticos.
        * **Demografía:** Distribución por sexo y edad.
        * **Metodología:** Efectividad de las pruebas aplicadas.
        
        **Acceda al menú lateral para comenzar el análisis técnico.**
        """)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png", caption="Visualización del virus")

# --- PANEL DE TRABAJO ---
else:
    st.title("📊 Panel de Análisis de Datos")
    
    # Filtro por departamento
    depts = st.multiselect("Seleccione Departamentos:", options=df['DEPARTAMENTO'].unique(), default=df['DEPARTAMENTO'].unique()[:5])
    filtered_df = df[df['DEPARTAMENTO'].isin(depts)]

    # Tabs para organización profesional
    tab1, tab2 = st.tabs(["📈 Gráficos de Análisis", "📖 Documentación"])

    with tab1:
        # Gráfico 1: Casos por Departamento
        st.subheader("Distribución Regional")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(data=filtered_df, y='DEPARTAMENTO', order=filtered_df['DEPARTAMENTO'].value_counts().index, palette="viridis", ax=ax)
        st.pyplot(fig)
        st.info("💡 Ayuda: Este gráfico muestra la carga de casos por departamento seleccionado.")

        st.divider()

        # Gráfico 2: Evolución Temporal
        st.subheader("Evolución de Casos")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        daily_cases = filtered_df.groupby('FECHA_RESULTADO').size()
        sns.lineplot(x=daily_cases.index, y=daily_cases.values, color="red", ax=ax2)
        st.pyplot(fig2)
        st.info("💡 Ayuda: Representa la tendencia temporal de contagios confirmados.")

    with tab2:
        st.markdown("""
        ### Ficha Técnica
        * **Dataset:** Peru COVID-19 (August 2020)
        * **Variables analizadas:** DEPARTAMENTO, FECHA_RESULTADO, SEXO, METODODX.
        * **Procesamiento:** Datos filtrados dinámicamente según la selección del usuario en el sidebar.
        """)
        st.dataframe(filtered_df.head(10))

st.sidebar.markdown("---")
st.sidebar.write("Realizado por: **Juan Jose Sánchez**")
