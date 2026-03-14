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

# 2. Carga de datos desde Kaggle
@st.cache_data
def cargar_datos():
    try:
        path = kagglehub.dataset_download("martinclark/peru-covid19-august-2020")
        archivos = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not archivos:
            return None
        df = pd.read_csv(os.path.join(path, archivos[0]))
        if 'FECHA_RESULTADO' in df.columns:
            df['FECHA_RESULTADO'] = pd.to_datetime(df['FECHA_RESULTADO'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

df = cargar_datos()

# 3. Sidebar (Menú lateral)
with st.sidebar:
    st.title("TalentoTech")
    st.write("Nivel Integradores")
    seccion = st.radio("Ir a:", ["Landing Page", "Panel de Trabajo"])
    st.divider()
    st.write("👨‍💻 Autor: **Juan Jose Sánchez**")

# 4. Sección: Landing Page
if seccion == "Landing Page":
    st.title("📊 Análisis de Datos COVID-19 Perú")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Bienvenido al Proyecto Integrador")
        st.markdown("""
        Esta aplicación utiliza un dataset de **Kaggle** para analizar el impacto de la pandemia en Perú 
        hasta agosto de 2020. Como expertos en datos, exploraremos la distribución regional y demográfica.
        
        **Instrucciones:**
        - Navega al **Panel de Trabajo** para ver los gráficos.
        - Usa los filtros para seleccionar departamentos específicos.
        - Consulta la documentación técnica en las pestañas.
        """)
    
    with col2:
        # NOMBRE DE IMAGEN CORREGIDO AQUÍ:
        try:
            st.image("images1.jfif", caption="Estructura del virus SARS-CoV-2", use_container_width=True)
        except:
            st.warning("⚠️ No se pudo cargar 'images1.jfif'. Verifica que el nombre en GitHub sea exacto.")

# 5. Sección: Panel de Trabajo
else:
    st.title("📈 Panel de Análisis Técnico")
    
    if df is not None:
        # Filtros profesionales
        deptos = st.multiselect("Seleccione Departamentos:", 
                               options=list(df['DEPARTAMENTO'].unique()), 
                               default=df['DEPARTAMENTO'].unique()[:5])
        
        df_filt = df[df['DEPARTAMENTO'].isin(deptos)]
        
        tab1, tab2 = st.tabs(["📊 Gráficos Estadísticos", "📖 Documentación"])

        with tab1:
            # Gráfico 1: Seaborn Countplot
            st.subheader("Distribución de Casos por Departamento")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            sns.countplot(data=df_filt, y='DEPARTAMENTO', palette="viridis", ax=ax1)
            st.pyplot(fig1)
            st.info("💡 Este gráfico muestra el volumen total de contagios por cada región seleccionada.")

            st.divider()

            # Gráfico 2: Distribución por Género
            st.subheader("Proporción por Sexo")
            fig2, ax2 = plt.subplots()
            counts = df_filt['SEXO'].value_counts()
            plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
            st.pyplot(fig2)
            st.info("💡 Muestra la distribución porcentual entre hombres y mujeres en la muestra filtrada.")

        with tab2:
            st.markdown("### Detalles del Dataset")
            st.write("Datos procesados del Ministerio de Salud (MINSA) de Perú.")
            st.dataframe(df_filt.head(20))
    else:
        st.error("No se pudieron cargar los datos de Kaggle.")
