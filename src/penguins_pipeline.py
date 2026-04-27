# Funcion para cargar el archivo:

from __future__ import annotations
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def carga_datos(path='notebooks/02_limpieza/penguins_limpio.csv'):
    return pd.read_csv(path)

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:

    # Filtro por isla
    filtro_isla = st.sidebar.multiselect(
        "Filtrar por isla:",
        df['Island'].unique()
    )

    # Si no hay filtro, devolvemos el df original
    if not filtro_isla:
        st.info("Selecciona una isla para ver el resumen.")
        return df

    # Filtrar el dataframe
    datos_filtrados = df[df['Island'].isin(filtro_isla)]

    # Crear resumen por especie
    resumen = datos_filtrados.groupby("Species")[[
        "Body Mass (g)",
        "Culmen Length (mm)",
        "Culmen Depth (mm)",
        "Flipper Length (mm)"
    ]].mean().round(2)

    # Añadir número de pingüinos por especie
    resumen["Nº Pingüinos"] = datos_filtrados.groupby("Species").size()

    # Mostrar tabla
    st.dataframe(resumen)

    return datos_filtrados

# Filtro por especie
def apply_filters_especies(df: pd.DataFrame) -> pd.DataFrame:
    filtro_especie = st.sidebar.multiselect(
        "Filtrar por especie:",
        df['Species'].unique()
    )

    # Si no hay filtro, devolvemos el df original
    if not filtro_especie:
        st.info("Selecciona una especie para ver el resumen.")
        return df

    # Filtrar el dataframe
    datos_filtrados = df[df['Species'].isin(filtro_especie)]

    # Crear resumen por isla
    resumen = datos_filtrados.groupby("Island")[[
        "Body Mass (g)",
        "Culmen Length (mm)",
        "Culmen Depth (mm)",
        "Flipper Length (mm)"
    ]].mean().round(2)

    # Añadir número de pingüinos por isla
    resumen["Nº Pingüinos"] = datos_filtrados.groupby("Island").size()

    # Mostrar tabla
    st.dataframe(resumen)

    return datos_filtrados

def grafico_masa_por_especie(df):
    fig = px.bar(
        df,
        x="Species",
        y="Body Mass (g)",
        color="Sex",
        barmode="group"
    )
    fig.update_layout(title="Masa corporal por especie y sexo")
    st.plotly_chart(fig)


def distribucion_especie(df):
    counts = df["Species"].value_counts().reset_index()
    counts.columns = ["Species", "Count"]

    fig = px.pie(
        counts,
        names="Species",
        values="Count",
        title="Distribución de pingüinos por especie"
    )

    st.plotly_chart(fig)

def graficos_lmplot(df):
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

def heatmap_correlaciones(df):
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



def compute_kpis(df: pd.DataFrame) -> dict[str, int]:
    num_machos = df[df["Sex"].str.upper() == "MALE"].shape[0]
    num_hembras = df[df["Sex"].str.upper() == "FEMALE"].shape[0]

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


    return {"rows": int(len(df)),"species": int(df["species"].nunique()) if "species" in df.columns else 0,"islands": int(df["island"].nunique()) if "island" in df.columns else 0,}
