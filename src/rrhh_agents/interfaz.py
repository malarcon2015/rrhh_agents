# interfaz.py
import streamlit as st
from io import StringIO
import sys
from contextlib import redirect_stdout
from rrhh_agents.crew import RrhhAgents
from dotenv import load_dotenv
import re
import pandas as pd

load_dotenv()

def extraer_tabla_de_resultado(texto_resultado: str) -> pd.DataFrame:
    candidatos = []
    bloques = texto_resultado.strip().split('\n\n')

    for bloque in bloques:
        lineas = bloque.strip().split('\n')
        if not lineas or len(lineas) < 2:
            continue

        header = lineas[0].strip()
        nombre = header.split('-')[0].strip('1234567890. ').strip()
        afinidad = header.split('-')[1].strip() if '-' in header else ''

        detalles = {}
        for linea in lineas[1:]:
            if ':' in linea:
                clave, valor = linea.strip().split(':', 1)
                detalles[clave.strip()] = valor.strip()

        candidato = {
            'Nombre': nombre,
            #'Afinidad': afinidad,
            **detalles
        }
        candidatos.append(candidato)

    return pd.DataFrame(candidatos)

def limpiar_headers_y_ansi(texto: str) -> str:
    # Eliminar códigos ANSI
    texto = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', texto)
    # Reemplazar encabezados Markdown tipo # y ##
    texto = re.sub(r'^#{1,6} ', '', texto, flags=re.MULTILINE)
    return texto

st.set_page_config(layout="wide")
st.title("👥 Selección de Talento")

# Layout: tres columnas
col1, col2, col3 = st.columns([1, 2, 0.01])

with col1:
    st.header("🎯 Ingresá la oferta laboral")
    oferta_manual = st.text_area("Oferta laboral (manual o copiada de LinkedIn)", height=300)
    sheet_url = st.text_input("🔗 URL de Google Sheet con candidatos")
    ejecutar = st.button("🚀 Ejecutar Flujo")

if ejecutar:
    with col2:
        st.header("🧠 Pensamientos de los agentes")
        pensamiento_output = StringIO()
        with redirect_stdout(pensamiento_output):
            try:
                resultado = RrhhAgents().crew().kickoff(inputs={
                    "oferta_manual": oferta_manual,
                    "sheet_url": sheet_url
                })
            except Exception as e:
                resultado = f"❌ Error durante la ejecución: {e}"

        pensamiento_limpio = limpiar_headers_y_ansi(pensamiento_output.getvalue())

        scrollable_output = f"""
        <div style="
            height: 500px;
            overflow-y: auto;
            padding: 10px;
            background-color: #111;
            color: #eee;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            line-height: 1.4;
            white-space: pre-wrap;
        ">
        <pre>{pensamiento_limpio}</pre>
        </div>
        """
        st.markdown(scrollable_output, unsafe_allow_html=True)

    # ✅ Resultado final en ancho completo debajo de las columnas
    st.markdown("---")
    st.header("✅ Resultado final (tabla de candidatos seleccionados)")

    try:
        texto_resultado = str(resultado.output) if hasattr(resultado, "output") else str(resultado)
        df_resultado = extraer_tabla_de_resultado(texto_resultado)
        st.dataframe(df_resultado, use_container_width=True)
    except Exception as e:
        st.text_area("Resultado sin procesar", value=str(resultado), height=400)
        st.warning(f"No se pudo convertir a tabla: {e}")