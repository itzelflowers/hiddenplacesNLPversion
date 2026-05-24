import re

# --- STOPWORDS EN ESPAÑOL ---
STOPWORDS = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante",
    "e", "el", "ella", "ellas", "ellos", "en", "entre", "era", "es", "esa",
    "esas", "ese", "eso", "esos", "esta", "estas", "este", "esto", "estos",
    "fue", "han", "has", "hasta", "hay", "he", "la", "las", "le", "les",
    "lo", "los", "me", "mi", "mis", "muy", "más", "ni", "no", "nos",
    "o", "otro", "para", "pero", "por", "que", "quien", "se", "si", "sin",
    "sobre", "son", "su", "sus", "también", "te", "tengo", "ti", "toda",
    "todas", "todo", "todos", "tu", "tus", "un", "una", "unas", "unos",
    "ya", "yo", "él", "ésta", "éstas", "éste", "éstos"
}

# --- DICCIONARIO DE LEMATIZACIÓN ---
# Forma conjugada/plural → forma base
LEMAS = {
    # Verbos comunes
    "comiendo": "comer", "comí": "comer", "comimos": "comer", "comieron": "comer",
    "fui": "ir", "fuimos": "ir", "fueron": "ir",
    "estuve": "estar", "estuvimos": "estar", "estuvieron": "estar",
    "ayudaron": "ayudar", "ayudó": "ayudar", "ayudamos": "ayudar",
    "atendieron": "atender", "atendió": "atender",
    "recomiendo": "recomendar", "recomendé": "recomendar", "recomendamos": "recomendar",
    "llegamos": "llegar", "llegué": "llegar", "llegaron": "llegar",
    "visitamos": "visitar", "visité": "visitar", "visitaron": "visitar",
    "subimos": "subir", "subí": "subir", "subieron": "subir",
    "bajamos": "bajar", "bajé": "bajar", "bajaron": "bajar",
    # Sustantivos plurales
    "rampas": "rampa", "escalones": "escalón", "elevadores": "elevador",
    "restaurantes": "restaurante", "lugares": "lugar", "opiniones": "opinión",
    "meseros": "mesero", "platillos": "platillo", "precios": "precio",
    "sillas": "silla", "ruedas": "rueda", "muletas": "muleta",
    "museos": "museo", "parques": "parque", "jardines": "jardín",
    # Adjetivos
    "amables": "amable", "accesibles": "accesible", "bonitos": "bonito",
    "lindos": "lindo", "ricos": "rico", "deliciosos": "delicioso",
    "limpios": "limpio", "cómodos": "cómodo"
}

def tokenizar(texto: str) -> list:
    """Divide el texto en palabras limpias."""
    # Convertir a minúsculas
    texto = texto.lower()
    # Quitar caracteres especiales y números, dejar solo letras y espacios
    texto = re.sub(r'[^a-záéíóúüñ\s]', ' ', texto)
    # Dividir en tokens
    tokens = texto.split()
    return tokens

def quitar_stopwords(tokens: list) -> list:
    """Elimina palabras sin significado."""
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

def lematizar(tokens: list) -> list:
    """Reduce palabras a su forma base usando el diccionario."""
    return [LEMAS.get(t, t) for t in tokens]

def preprocesar(texto: str) -> list:
    """
    Pipeline completo:
    tokenizar → quitar stopwords → lematizar
    """
    tokens = tokenizar(texto)
    tokens = quitar_stopwords(tokens)
    tokens = lematizar(tokens)
    return tokens

def preprocesar_opiniones(opiniones) -> str:
    """
    Preprocesa todas las opiniones y retorna texto limpio
    listo para BERT o matching de palabras.
    """
    if not opiniones:
        return ""

    if isinstance(opiniones, list):
        texto_completo = " ".join([op for op in opiniones if op])
    elif isinstance(opiniones, dict):
        texto_completo = " ".join(opiniones.values())
    else:
        return ""

    tokens = preprocesar(texto_completo)
    return " ".join(tokens)