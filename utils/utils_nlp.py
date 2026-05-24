from transformers import pipeline
import streamlit as st

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
        "precio", "caro", "barato", "económico", "cobran", "costo", "vale"
    ],
    "ubicación": [
        "ubicación", "llegar", "transporte", "estacionamiento", "céntrico", "cerca"
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
    """
    Hace matching de palabras clave de accesibilidad.
    Retorna score por categoría y menciones encontradas.
    """
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
    """
    Hace matching de aspectos generales para lugares de Comida,
    Cultura y Entretenimiento.
    Retorna lista de aspectos encontrados.
    """
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
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception:
        return pipeline("text-generation", model="gpt2")

def generar_resumen(opiniones) -> str:
    """
    Genera un resumen con BERT de las opiniones brutas.
    Maneja lista o dict.
    """
    if not opiniones:
        return "Sin opiniones disponibles."

    if isinstance(opiniones, list):
        texto = " ".join([op for op in opiniones if op])
    elif isinstance(opiniones, dict):
        texto = " ".join(opiniones.values())
    else:
        return "Sin opiniones disponibles."

    texto = texto[:1024]
    summarizer = cargar_modelo()
    resumen = summarizer(texto, max_length=130, min_length=30, do_sample=False)
    
    resultado = resumen[0]
    return resultado.get('summary_text') or resultado.get('generated_text', 'Sin resumen disponible.')