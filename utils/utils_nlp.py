#para los comentarios 
from transformers import pipeline
import streamlit as st

# --- DICCIONARIO DE PALABRAS CLAVE POR CATEGORÍA ---
CATEGORIAS_ACCESIBILIDAD = {
    "rampas": [
        "rampa", "rampas", "acceso", "entrada accesible", "desnivel"
    ],
    "elevadores": [
        "elevador", "elevadores", "ascensor", "lift", "sube"
    ],
    "sillas_ruedas": [
        "silla de ruedas", "silla ruedas", "wheelchair", "movilidad reducida", "discapacidad"
    ],
    "estacionamiento": [
        "estacionamiento accesible", "cajón", "espacio discapacitados", "parking accesible"
    ],
    "asistencia": [
        "ayuda", "asistencia", "apoyo", "personal", "amable", "ayudaron"
    ]
}

def calcular_score_accesibilidad(opiniones: dict) -> dict:
    """
    Hace matching de palabras clave en las opiniones.
    Retorna un score por categoría (0-10) y menciones encontradas.
    """
    if not opiniones:
        return {}

    # Unir todas las opiniones en minúsculas
    texto_completo = " ".join(opiniones.values()).lower()

    resultados = {}
    for categoria, palabras_clave in CATEGORIAS_ACCESIBILIDAD.items():
        menciones = [p for p in palabras_clave if p in texto_completo]
        # Score: cuántas palabras clave se mencionaron / total posible * 10
        score = round((len(menciones) / len(palabras_clave)) * 10, 1)
        resultados[categoria] = {
            "score": score,
            "menciones": menciones
        }

    return resultados

@st.cache_resource
def cargar_modelo():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def generar_resumen(opiniones: dict) -> str:
    """
    Genera un resumen con BERT de las opiniones brutas.
    """
    if not opiniones:
        return "Sin opiniones disponibles."

    summarizer = cargar_modelo()
    texto = " ".join(opiniones.values())
    texto = texto[:1024]  # límite de tokens

    resumen = summarizer(texto, max_length=130, min_length=30, do_sample=False)
    return resumen[0]['summary_text']