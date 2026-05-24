import re
import unicodedata


def normalizar_texto(texto):
    """
    Convierte texto a minúsculas, elimina acentos y limpia espacios.
    """
    if texto is None:
        return ""

    texto = str(texto).lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9ñ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


TIPOS_LUGAR = {
    "comida": [
        "comida", "comer", "restaurante", "cafeteria", "cafe",
        "desayunar", "cenar", "almorzar", "torta", "tacos"
    ],
    "cultura": [
        "cultura", "cultural", "museo", "arte", "exposicion",
        "galeria", "historia", "teatro", "biblioteca"
    ],
    "entretenimiento": [
        "entretenimiento", "diversion", "cine", "parque",
        "pasear", "turismo", "visitar", "familia"
    ],
}


ACCESIBILIDAD = {
    "rampas": [
        "rampa", "rampas", "sin escaleras", "entrada accesible",
        "desnivel", "facil acceso"
    ],
    "elevadores": [
        "elevador", "elevadores", "ascensor", "ascensores"
    ],
    "sillas_ruedas": [
        "silla de ruedas", "sillas de ruedas", "movilidad reducida",
        "discapacidad", "persona con discapacidad", "acceso accesible"
    ],
    "estacionamiento": [
        "estacionamiento", "parking", "cajon", "auto", "coche",
        "carro", "valet"
    ],
    "asistencia": [
        "asistencia", "ayuda", "apoyo", "personal amable",
        "personal atento", "acompanamiento"
    ],
}


CONCEPTOS_NATURALES = {
    "adulto_mayor": [
        "abuelita", "abuelito", "abuela", "abuelo",
        "adulto mayor", "persona mayor", "mi mama", "mi papa",
        "camina lento", "camina poco"
    ],
    "accesible": [
        "accesible", "accesibilidad", "comodo", "facil de entrar",
        "facil acceso", "incluyente", "inclusivo"
    ],
}


ALCALDIAS_CDMX = [
    "alvaro obregon",
    "azcapotzalco",
    "benito juarez",
    "coyoacan",
    "cuajimalpa",
    "cuauhtemoc",
    "gustavo a madero",
    "iztacalco",
    "iztapalapa",
    "magdalena contreras",
    "miguel hidalgo",
    "milpa alta",
    "tlahuac",
    "tlalpan",
    "venustiano carranza",
    "xochimilco",
]


def valor_si_no(valor):
    """
    Convierte valores como 'Sí', 'Si', 'No', True, False a booleano.
    """
    texto = normalizar_texto(valor)

    if texto in ["si", "sí", "true", "1", "yes"]:
        return True

    return False


def unir_opiniones(opiniones):
    """
    Convierte opiniones_brutas en texto plano.
    """
    if opiniones is None:
        return ""

    if isinstance(opiniones, list):
        return " ".join(str(op) for op in opiniones)

    if isinstance(opiniones, dict):
        return " ".join(str(v) for v in opiniones.values())

    return str(opiniones)


def construir_documento_lugar(lugar):
    """
    Convierte un lugar en un documento textual para búsqueda.
    """
    nombre = lugar.get("Place", "")
    ubicacion = lugar.get("Location", "")
    tipo = lugar.get("bss_type", "")
    resumen = lugar.get("resumen_nlp", "")
    opiniones = unir_opiniones(lugar.get("opiniones_brutas", ""))

    accesibilidad = []

    for campo in ["rampas", "elevadores", "sillas_ruedas", "estacionamiento", "asistencia"]:
        if valor_si_no(lugar.get(campo, "")):
            accesibilidad.append(campo.replace("_", " "))

    texto_accesibilidad = " ".join(accesibilidad)

    documento = f"""
    {nombre}
    {ubicacion}
    {tipo}
    {texto_accesibilidad}
    {resumen}
    {opiniones}
    """

    return normalizar_texto(documento)


def extraer_intencion_consulta(query):
    """
    Detecta tipo de lugar, accesibilidad y ubicación desde la consulta.
    """
    query_norm = normalizar_texto(query)

    intencion = {
        "tipos": [],
        "accesibilidad": [],
        "conceptos": [],
        "ubicaciones": [],
        "query_norm": query_norm
    }

    for tipo, palabras in TIPOS_LUGAR.items():
        for palabra in palabras:
            if normalizar_texto(palabra) in query_norm:
                intencion["tipos"].append(tipo)
                break

    for campo, palabras in ACCESIBILIDAD.items():
        for palabra in palabras:
            if normalizar_texto(palabra) in query_norm:
                intencion["accesibilidad"].append(campo)
                break

    for concepto, palabras in CONCEPTOS_NATURALES.items():
        for palabra in palabras:
            if normalizar_texto(palabra) in query_norm:
                intencion["conceptos"].append(concepto)
                break

    for alcaldia in ALCALDIAS_CDMX:
        if alcaldia in query_norm:
            intencion["ubicaciones"].append(alcaldia)

    # Si detecta adulto mayor o accesible, reforzamos accesibilidad general
    if "adulto_mayor" in intencion["conceptos"] or "accesible" in intencion["conceptos"]:
        for campo in ["rampas", "elevadores", "sillas_ruedas", "asistencia"]:
            if campo not in intencion["accesibilidad"]:
                intencion["accesibilidad"].append(campo)

    return intencion


def calcular_score_lugar(query, lugar, intencion):
    """
    Calcula un puntaje de relevancia para un lugar.
    """
    score = 0
    razones = []

    documento = construir_documento_lugar(lugar)
    query_norm = intencion["query_norm"]

    tipo_lugar = normalizar_texto(lugar.get("bss_type", ""))
    ubicacion_lugar = normalizar_texto(lugar.get("Location", ""))

    # 1. Coincidencia por tipo de lugar
    for tipo in intencion["tipos"]:
        if tipo == tipo_lugar:
            score += 30
            razones.append(f"Coincide con tipo de lugar: {tipo}")

    # 2. Coincidencia por ubicación
    for ubicacion in intencion["ubicaciones"]:
        if ubicacion in ubicacion_lugar:
            score += 25
            razones.append(f"Coincide con ubicación: {ubicacion}")

    # 3. Coincidencia por accesibilidad en metadatos
    for campo in intencion["accesibilidad"]:
        if valor_si_no(lugar.get(campo, "")):
            score += 25
            razones.append(f"Cuenta con {campo.replace('_', ' ')}")
        else:
            score -= 20
            razones.append(f"No cuenta con {campo.replace('_', ' ')} solicitado")

    # 4. Coincidencia de palabras de la consulta contra el documento
    palabras_query = [
        p for p in query_norm.split()
        if len(p) > 3
    ]

    coincidencias = 0

    for palabra in palabras_query:
        if palabra in documento:
            coincidencias += 1

    if palabras_query:
        keyword_score = (coincidencias / len(palabras_query)) * 25
        score += keyword_score

        if coincidencias > 0:
            razones.append(f"Coincidencias de texto: {coincidencias}")

    # 5. Pequeño bonus por tener texto NLP/resumen/opiniones
    if lugar.get("resumen_nlp"):
        score += 5

    if lugar.get("opiniones_brutas"):
        score += 5

    return score, razones


def recuperar_lugares(query, lugares, top_k=10):
    """
    Recupera lugares relevantes a partir de una consulta en lenguaje natural.
    Este es un retriever básico por keywords y metadatos.
    """
    if not query or not lugares:
        return []

    intencion = extraer_intencion_consulta(query)

    resultados = []

    for lugar in lugares:
        if not isinstance(lugar, dict):
            continue

        score, razones = calcular_score_lugar(query, lugar, intencion)

        if score >= 30:
            resultado = lugar.copy()
            resultado["score_retriever"] = round(score, 2)
            resultado["razones_retriever"] = razones
            resultados.append(resultado)

    resultados = sorted(
        resultados,
        key=lambda x: x.get("score_retriever", 0),
        reverse=True
    )

    return resultados[:top_k]