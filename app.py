import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from src.penguins_pipeline import carga_datos, apply_filters


#Configuracion de la pagina

st.set_page_config(page_title="Pinguinos", #titulo de la pagina
                   layout="wide", #para que ocupe el ancho de la ventana"
                   page_icon="🐧")

from PIL import Image
import streamlit as st

# Cargar imagen local
cabecera = Image.open("imagen_pinguinos.png")

# Mostrarla como banner
st.image(cabecera)

st.title("Analisis del grupo 4")

# Texto a poner debajo del titulo
with st.expander("👥 Integrantes del equipo"):
    st.markdown("""
    **Chiara Contreras**  
    **Jenireé Tovar**  
    **Lucia Llaneza**  
    **Michelle Olivares**  
    **Sara Bailon**  
    """)


# Carga del dataset

df = carga_datos()

#Creacion de la barra lateral
opcion = st.sidebar.selectbox(
    "Selecciona qué quieres ver:",
    [
        "Nada",
        "Gráfico: Masa corporal por especie",
        "Gráfico: Distribución por especie (pie chart)",
        "Gráficos lmplot",
        "Tabla filtrada",
        "Heatmap de correlaciones"
    ]
)

if opcion == "Gráfico: Masa corporal por especie":
    fig = px.bar(
        df,
        x="Species",
        y="Body Mass (g)",
        color="Sex",
        barmode="group"
    )
    fig.update_layout(title="Masa corporal por especie y sexo")
    st.plotly_chart(fig)

if opcion == "Gráfico: Distribución por especie (pie chart)":
    counts = df["Species"].value_counts().reset_index()
    counts.columns = ["Species", "Count"]

    fig = px.pie(
        counts,
        names="Species",
        values="Count",
        title="Distribución de pingüinos por especie"
    )

    st.plotly_chart(fig)

if opcion == "Gráficos lmplot":
    tab1, tab2, tab3 = st.tabs([
        "Culmen Length vs Body Mass",
        "Culmen Depth vs Body Mass",
        "Flipper Length vs Body Mass"
    ])

    with tab1:
        st.subheader("Relación entre Culmen Length y Body Mass")
        fig1 = sns.lmplot(
            data=df,
            x='Culmen Length (mm)',
            y='Body Mass (g)',
            hue='Species'
        )
        st.pyplot(fig1)

    with tab2:
        st.subheader("Relación entre Culmen Depth y Body Mass")
        fig2 = sns.lmplot(
            data=df,
            x='Culmen Depth (mm)',
            y='Body Mass (g)',
            hue='Species'
        )
        st.pyplot(fig2)

    with tab3:
        st.subheader("Relación entre Flipper Length y Body Mass")
        fig3 = sns.lmplot(
            data=df,
            x='Flipper Length (mm)',
            y='Body Mass (g)',
            hue='Species'
        )
        st.pyplot(fig3)

if opcion == "Tabla filtrada":
    apply_filters(df)


if opcion == "Heatmap de correlaciones":
    columnas = [
        "Culmen Length (mm)",
        "Culmen Depth (mm)",
        "Flipper Length (mm)",
        "Body Mass (g)"
    ]

    corr = df[columnas].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        fmt='.2f',
        ax=ax
    )
    ax.set_title("Correlaciones entre variables morfológicas")
    st.pyplot(fig)


# Crear un mapa con las islas
m = folium.Map(location=[-62.1, -57.9], zoom_start=7)

# Centro del mapa (aprox. zona de las islas)
m = folium.Map(location=[-65.0, -64.5], zoom_start=8)

st.subheader("🗺️ Mapa de las islas analizadas")

title_html = '''
     <h3 align="center" style="font-size:20px"><b>Mapa de las islas analizadas</b></h3>
     '''
m.get_root().html.add_child(folium.Element(title_html))

# Marcadores de las islas
folium.Marker(
    [-65.4333, -65.5000],
    popup="Isla Biscoe",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

folium.Marker(
    [-64.7333, -64.2333],
    popup="Isla Dream",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(m)

folium.Marker(
    [-64.7667, -64.0833],
    popup="Isla Torgersen",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Mostrar mapa en Streamlit
st_folium(m, width=700, height=500)

# Añadir metricas generales: 

num_machos = df[df["Sex"].str.upper() == "MALE"].shape[0]
num_hembras = df[df["Sex"].str.upper() == "FEMALE"].shape[0]

with st.expander("📊 Métricas generales del dataset"):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric('Pingüinos analizados', df.shape[0])
    with col2:
        st.metric("Numero de islas", df['Island'].nunique())
    with col3:
        st.metric('Número de especies', df['Species'].nunique())
    with col4:
        st.metric("Pingüinos machos", num_machos)
    with col5:
        st.metric("Pingüinos hembras", num_hembras)


