import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Análisis COVID-19 Perú - Juan Jose Sánchez",
    page_icon="📊",
    layout="wide"
)

# 2. Función para descargar y cargar datos
@st.cache_data
def cargar_datos():
    try:
        path = kagglehub.dataset_download("martinclark/peru-covid19-august-2020")
        archivo_csv = [f for f in os.listdir(path) if f.endswith('.csv')][0]
        full_path = os.path.join(path, archivo_csv)
        df = pd.read_csv(full_path)
        if 'FECHA_RESULTADO' in df.columns:
            df['FECHA_RESULTADO'] = pd.to_datetime(df['FECHA_RESULTADO'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error al conectar con los datos: {e}")
        return None

df = cargar_datos()

# 3. Navegación Lateral
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/82/SARS-CoV-2_without_background.png", width=100)
    st.title("Talentotech")
    menu = st.radio("Secciones", ["Inicio", "Panel de Trabajo"])
    st.divider()
    st.write("Autor: **Juan Jose Sánchez**")

# 4. Sección: Inicio (Landing Page)
if menu == "Inicio":
    st.title("🦠 Análisis del COVID-19 en Perú")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Contexto del Dataset
        Como experto en análisis de datos, este panel explora la base de datos de casos positivos en Perú hasta agosto de 2020. 
        El objetivo es aplicar los conocimientos integradores del curso de **Talentotech** para visualizar el impacto regional y demográfico.
        
        **Instrucciones:**
        1. Seleccione 'Panel de Trabajo' en el menú lateral.
        2. Use los filtros para segmentar por región.
        3. Consulte la documentación en las pestañas internas.
        """)
    with col2:
        st.image("https://cdn.pixabay.com/photo/2020/04/19/07/13/coronavirus-5062217_1280.png")

# 5. Sección: Panel de Trabajo
else:
    st.title("📈 Centro de Análisis Estadístico")
    
    if df is not None:
        departamentos = st.multiselect(
            "Filtrar Departamentos:", 
            options=list(df['DEPARTAMENTO'].unique()),
            default=df['DEPARTAMENTO'].unique()[:5]
        )
        
        df_filt = df[df['DEPARTAMENTO'].isin(departamentos)]
        tab_graf, tab_info = st.tabs(["📊 Gráficos Seaborn", "📖 Documentación"])

        with tab_graf:
            # Gráfico de Barras
            st.subheader("Contagios por Región")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            sns.countplot(data=df_filt, y='DEPARTAMENTO', palette="mako", ax=ax1)
            st.pyplot(fig1)
            st.info("💡 Ayuda: Visualización de la magnitud de contagios por departamento seleccionado.")

            st.divider()

            # Gráfico de Torta
            st.subheader("Distribución por Género")
            fig2, ax2 = plt.subplots()
            sex_data = df_filt['SEXO'].value_counts()
            plt.pie(sex_data, labels=sex_data.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
            st.pyplot(fig2)
            st.info("💡 Ayuda: Este gráfico circular permite identificar qué género reportó más casos positivos.")

        with tab_info:
            st.markdown("### Información del Procesamiento")
            st.write("Los datos han sido pre-procesados para asegurar que las fechas y categorías sean consistentes.")
            st.dataframe(df_filt.head(10))
    else:
        st.error("Dataset no encontrado.")
