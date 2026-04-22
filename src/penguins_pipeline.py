# Funcion para cargar el archivo:

from __future__ import annotations
import pandas as pd
import streamlit as st

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