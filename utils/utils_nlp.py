from transformers import pipeline
import streamlit as st
from utils.preprocesamiento import preprocesar_opiniones

# --- ACCESIBILIDAD (para lugares de Salud) ---
CATEGORIAS_ACCESIBILIDAD = {
    "rampas": [
        "rampa", "rampas", "acceso", "entrada accesible", "desnivel",
        "escalón", "escalones", "pendiente"
    ],
    "elevadores": [
        "elevador", "elevadores", "ascensor", "lift", "sube",
        "subir", "piso", "nivel"
    ],
    "sillas_ruedas": [
        "silla de ruedas", "silla ruedas", "wheelchair", "movilidad reducida",
        "discapacidad", "discapacitado", "accesible", "accesibilidad"
    ],
    "estacionamiento": [
        "estacionamiento accesible", "cajón", "espacio discapacitados",
        "parking accesible", "estacionamiento", "parking"
    ],
    "asistencia": [
        "ayuda", "asistencia", "apoyo", "personal", "amable", "ayudaron",
        "atención", "servicio", "atendieron", "trato", "amabilidad"
    ]
}

# --- ASPECTOS GENERALES (para Comida, Cultura, Entretenimiento) ---
ASPECTOS_GENERALES = {
    "experiencia": [
        "increíble", "recomendable", "vale la pena", "bonito", "hermoso",
        "excelente", "maravilloso", "espectacular", "agradable", "lindo"
    ],
    "servicio": [
        "atención", "amable", "servicio", "trato", "personal",
        "amabilidad", "atentos", "rápido", "eficiente"
    ],
    "accesibilidad": [
        "rampa", "elevador", "silla", "accesible", "discapacidad", "movilidad"
    ],
    "precio": [
        "caro", "barato", "económico", "cobran", "costo", 
        "precios altos", "precios bajos", "vale lo que cuesta", "costoso"
    ],
    "ubicación": [
        "fácil llegar", "bien ubicado", "lejos", "cerca del metro",
        "difícil llegar", "céntrico", "zona", "colonia"
    ]
}

def texto_desde_opiniones(opiniones):
    """Convierte opiniones (lista o dict) a texto plano en minúsculas."""
    if not opiniones:
        return ""
    if isinstance(opiniones, list):
        return " ".join([op for op in opiniones if op]).lower()
    elif isinstance(opiniones, dict):
        return " ".join(opiniones.values()).lower()
    return ""

def calcular_score_accesibilidad(opiniones) -> dict:
    if not opiniones:
        return {}
    texto_completo = texto_desde_opiniones(opiniones)
    resultados = {}
    for categoria, palabras_clave in CATEGORIAS_ACCESIBILIDAD.items():
        menciones = [p for p in palabras_clave if p in texto_completo]
        score = round((len(menciones) / len(palabras_clave)) * 10, 1)
        resultados[categoria] = {
            "score": score,
            "menciones": menciones
        }
    return resultados

def calcular_aspectos_generales(opiniones) -> list:
    if not opiniones:
        return []
    texto_completo = texto_desde_opiniones(opiniones)
    encontrados = []
    for aspecto, palabras in ASPECTOS_GENERALES.items():
        menciones = [p for p in palabras if p in texto_completo]
        if menciones:
            encontrados.append({
                "aspecto": aspecto,
                "menciones": menciones
            })
    return encontrados

@st.cache_resource
def cargar_modelo():
    try:
        return pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")
    except Exception:
        return pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    
def generar_resumen(opiniones) -> str:
    if not opiniones:
        return "Sin opiniones disponibles."

    texto_limpio = preprocesar_opiniones(opiniones)
    if not texto_limpio:
        return "Sin opiniones disponibles."

    texto_limpio = texto_limpio[:1024]
    summarizer = cargar_modelo()
    resumen = summarizer(
        texto_limpio, 
         max_length=400,
         min_length=100,   
         do_sample=False,
         truncation=True
)

    resultado = resumen[0]
    return resultado.get('summary_text') or resultado.get('generated_text', 'Sin resumen disponible.')