import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from src.penguins_pipeline import carga_datos, apply_filters, grafico_masa_por_especie, distribucion_especie, graficos_lmplot, heatmap_correlaciones, compute_kpis, apply_filters_especies


from PIL import Image
import streamlit as st

#Configuracion de la pagina

st.set_page_config(page_title="Grupazo 4", #titulo de la pagina
                   layout="wide", #para que ocupe el ancho de la ventana"
                   page_icon="🐧")


import base64
from PIL import Image

def imagen_a_base64(imagen_pinguinos):
    with open(imagen_pinguinos, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_b64 = imagen_a_base64("Imagenes/imagen_pinguinos.png")

st.markdown(f"""
    <style>
    /* Elimina padding del contenedor /
    .block-container {{
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 0rem;
    }}
    / Oculta header gris de Streamlit /
    header[data-testid="stHeader"] {{
        display: none;
    }}
    / El banner "escapa" del contenedor con márgenes negativos */
    .banner-wrapper {{
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        width: 100vw;
        max-height: 500px;
        overflow: hidden;
       
    }}
    .banner-wrapper img {{
        width: 100%;
        height: 500px;
        object-fit: cover;
        object-position: center;
        display: block;
    }}
    </style>
    <div class="banner-wrapper">
        <img src="data:image/png;base64,{img_b64}" />
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import base64

def set_background(Version_nocturna_del):
    with open(Version_nocturna_del, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("Imagenes/Version_nocturna_del.webp")

#Título debajo de la cabecera
st.title("Análisis del grupazo 4")

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
img_sidebar_b64 = imagen_a_base64("Imagenes/Pingu_fit.webp")

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/png;base64,{img_sidebar_b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
""", unsafe_allow_html=True)

#--- Caja 1: Visualizaciones ---
opcion_visual = st.sidebar.selectbox(
    "📊 Gráficos y Análisis:",
    [
        "Nada",
        "Heatmap de correlaciones",
        "Gráfico: Masa corporal por especie",
        "Gráfico: Distribución por especie (pie chart)",
        "Gráficos lmplot",
        
    ]
)

#--- Caja 2: Datos ---
opcion_datos = st.sidebar.selectbox(
    "📋 Datos y Tablas:",
    ["Nada", "Tabla filtrada"]
)

#--- Lógica para mostrar los Gráficos ---
if opcion_visual == "Gráfico: Masa corporal por especie":
    grafico_masa_por_especie(df)

elif opcion_visual == "Gráfico: Distribución por especie (pie chart)":
    distribucion_especie(df)

elif opcion_visual == "Gráficos lmplot":
    graficos_lmplot(df)

elif opcion_visual == "Heatmap de correlaciones":
    heatmap_correlaciones(df)

#--- Lógica para mostrar la Tabla ---
if opcion_datos == "Tabla filtrada":
    apply_filters(df)
    apply_filters_especies(df)
# Añadir metricas generales: 



with st.expander("📊 Métricas generales del dataset"):
    compute_kpis(df)


conteo_islas = df['Island'].value_counts().to_dict()
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
# Biscoe
folium.Marker(
    [-65.4333, -65.5000],
    popup=f"Isla Biscoe — {conteo_islas.get('Biscoe', 0)} 🐧",
    tooltip=f"Biscoe: {conteo_islas.get('Biscoe', 0)} 🐧",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Dream
folium.Marker(
    [-64.7333, -64.2333],
    popup=f"Isla Dream — {conteo_islas.get('Dream', 0)} 🐧",
    tooltip=f"Dream: {conteo_islas.get('Dream', 0)} 🐧",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(m)

# Torgersen
folium.Marker(
    [-64.7667, -64.0833],
    popup=f"Isla Torgersen — {conteo_islas.get('Torgersen', 0)} 🐧",
    tooltip=f"Torgersen: {conteo_islas.get('Torgersen', 0)} 🐧",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Mostrar mapa en Streamlit
st_folium(m, width=True, height=500)


import streamlit as st

st.markdown("<h1 style='text-align: center;'>🐧⛔ Limitaciones y Sesgos</h1>", unsafe_allow_html=True)
st.divider()

#Primera fila: El problema principal
st.error("### 🛑 Limitación Crítica: Comportamiento\nNo existen datos suficientes para concluir diferencias en migración, reproducción o anidación.")

#Segunda fila: Sesgos técnicos
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### ⚖️ Sesgos de Identificación")
        st.write("""
        
IDs Reutilizados: Imposible el seguimiento multianual.
Errores Sistemáticos: Identificación errónea persistente en las muestras.""")

with col2:
    with st.container(border=True):
        st.markdown("#### 🧬 Barrera Técnica")
        st.write("""
        
Conocimiento Específico: Datos como las columnas Delta requieren perfiles en biología marina para evitar especulaciones.""")

#Tercera fila: Propuesta de mejora
st.info("#### 📋 Propuesta para el Cliente\nImplementar una nomenclatura alfanumérica optimizada para garantizar trazabilidad y eliminar sesgos de información.")

import streamlit as st
 

st.markdown("""
<style>
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    .section-content {
        font-size: 0.92rem;
        line-height: 1.55;
        color: #374151;
        margin: 0;
    }
    .badge-evidencia      { color: #1d4ed8; }
    .badge-interpretacion { color: #7c3aed; }
    .badge-implicacion    { color: #b45309; }
    .badge-recomendacion  { color: #065f46; }

    .pill-evidencia      { background: #eff6ff; border-left: 4px solid #3b82f6; border-radius: 0 8px 8px 0; padding: 12px 14px; }
    .pill-interpretacion { background: #f5f3ff; border-left: 4px solid #8b5cf6; border-radius: 0 8px 8px 0; padding: 12px 14px; }
    .pill-implicacion    { background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 0 8px 8px 0; padding: 12px 14px; }
    .pill-recomendacion  { background: #ecfdf5; border-left: 4px solid #10b981; border-radius: 0 8px 8px 0; padding: 12px 14px; }

    div[data-testid="column"] { padding: 4px 8px; }
</style>
""", unsafe_allow_html=True)

# ── Datos ─────────────────────────────────────────────────────────────────────

hallazgos = [
    {
        "titulo": "Primer hallazgo — Individual IDs",
        "evidencia": "Observamos un patrón en los IDs individuales: aunque se pierdan los datos o aparezcan como nulos, en su gran mayoría hacen referencia a una pareja (macho/hembra).",
        "interpretacion": "El estudio se enfoca en parejas de pingüinos.",
        "implicacion": "Al tratarse de un dato muy relevante para el estudio, el cliente debe asegurar la calidad de este dato.",
        "recomendacion": "Asignar un número en el individual_ID (1 o 2) dependiendo de si se trata de un macho (ej. 1) o una hembra (ej. 2) para mantener la trazabilidad.",
    },
    {
        "titulo": "Segundo hallazgo — Desequilibrio por especies",
        "evidencia": "Existe una gran diferencia en la cantidad de datos analizados por especie. Chinstrap aporta solo el 20% de las muestras, mientras que Adelie y Gentoo suponen casi el 40% cada una.",
        "interpretacion": "El dataset no está equilibrado para hacer un análisis comparativo por especies.",
        "implicacion": "Para el cliente, las comparaciones entre especies no aportarán valor real.",
        "recomendacion": "Reconsiderar el muestreo de cada especie o especificar mejor si estos datos son relevantes para comparaciones futuras.",
    },
    {
        "titulo": "Tercer hallazgo — Concentración por islas",
        "evidencia": "La toma de muestras está concentrada en las islas Biscoe y Dream; la isla Torgersen supone únicamente el 13%.",
        "interpretacion": "El dataset es escaso para representar una distribución real entre islas.",
        "implicacion": "El análisis puede estar sesgado debido a esta distribución desigual.",
        "recomendacion": "Mejorar la calidad del dato para que las comparativas sean más fieles. Valorar si al cliente le interesa estudiar la presencia/ausencia de pingüinos entre islas en época de anidación e incubación.",
    },
    {
        "titulo": "Cuarto hallazgo — Similitud morfológica Adelie/Chinstrap",
        "evidencia": "Las especies Adelie y Chinstrap comparten características similares (profundidad del pico y longitud de la aleta), lo que las hace difíciles de separar para interpretar perfiles biológicos.",
        "interpretacion": "Al tener datos similares, las comparaciones entre estas dos especies no son relevantes.",
        "implicacion": "Si el objetivo es obtener diferencias observables entre estas especies, será necesario aportar otros datos.",
        "recomendacion": "Recoger datos más significativos que las diferencien, ampliar la toma de muestras y crear perfiles biológicos más completos para comparar la morfología de las especies.",
    },
    {
        "titulo": "Quinto hallazgo — Escasez de datos temporales",
        "evidencia": "Los datos temporales son muy limitados: solo cubren noviembre y principios de diciembre. No se dispone de información sobre la población anual de las islas.",
        "interpretacion": "Probablemente se trate de la época de mayor anidación y reproducción, pero no es posible concluir si la población aumenta o disminuye a lo largo del año.",
        "implicacion": "El cliente tendría datos más fieles del aumento o decrecimiento de la población si se ampliara el periodo de muestreo.",
        "recomendacion": "Mantener un seguimiento anual o estacional para ver la evolución de la distribución poblacional, incluyendo crías, adultos en época de reproducción y pingüinos mayores.",
    },
]

# ── UI ────────────────────────────────────────────────────────────────────────

st.markdown("## 🎯 Conclusiones y recomendaciones")

numeros = ["①", "②", "③", "④", "⑤"]

with st.expander("📋 Hallazgos", expanded=False):
    for i, h in enumerate(hallazgos):
        with st.expander(f"{numeros[i]} {h['titulo']}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    f'<div class="pill-evidencia">'
                    f'<p class="section-label badge-evidencia">🔍 Evidencia observada</p>'
                    f'<p class="section-content">{h["evidencia"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f'<div class="pill-interpretacion">'
                    f'<p class="section-label badge-interpretacion">🧠 Interpretación</p>'
                    f'<p class="section-content">{h["interpretacion"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    f'<div class="pill-implicacion">'
                    f'<p class="section-label badge-implicacion">💼 Implicación para el cliente</p>'
                    f'<p class="section-content">{h["implicacion"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col4:
                st.markdown(
                    f'<div class="pill-recomendacion">'
                    f'<p class="section-label badge-recomendacion">✅ Recomendación concreta</p>'
                    f'<p class="section-content">{h["recomendacion"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
