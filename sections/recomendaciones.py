# Importar librerías necesarias.
import streamlit as st

from utils.firebase import Firebase
from utils.retriever import recuperar_lugares

db = Firebase().getdb()


def obtener_lugares():
    """
    Obtiene los lugares desde Firebase y los convierte en lista de diccionarios.
    """
    lugares_data = db.child('Lugares').get().val()

    if not lugares_data:
        return []

    lugares = []

    for lugar_id, datos in lugares_data.items():
        if isinstance(datos, dict):
            datos["firebase_id"] = lugar_id
            lugares.append(datos)

    return lugares


def mostrar_lugar(lugar):
    """
    Muestra un lugar recomendado en Streamlit.
    """
    nombre = lugar.get("Place", "Lugar sin nombre")
    ubicacion = lugar.get("Location", "Ubicación no disponible")
    tipo = lugar.get("bss_type", "Tipo no disponible")

    st.subheader(nombre)

    st.write(f"**Tipo:** {tipo}")
    st.write(f"**Ubicación:** {ubicacion}")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.write(f"🦽 Silla: {lugar.get('sillas_ruedas', 'N/D')}")
    col2.write(f"🛗 Elevador: {lugar.get('elevadores', 'N/D')}")
    col3.write(f"♿ Rampas: {lugar.get('rampas', 'N/D')}")
    col4.write(f"🚗 Estac.: {lugar.get('estacionamiento', 'N/D')}")
    col5.write(f"🤝 Asistencia: {lugar.get('asistencia', 'N/D')}")

    if lugar.get("resumen_nlp"):
        st.write("**Resumen NLP:**")
        st.write(lugar.get("resumen_nlp"))

    if lugar.get("score_retriever") is not None:
        st.write(f"**Score de relevancia:** {lugar.get('score_retriever')}")

    razones = lugar.get("razones_retriever", [])

    if razones:
        with st.expander("¿Por qué aparece este resultado?"):
            for razon in razones:
                st.write(f"- {razon}")

    st.divider()


def app():
    st.title("Tus recomendaciones")
    st.write(
        "Busca lugares usando lenguaje natural. "
        "Por ejemplo: museo con rampa en Coyoacán, restaurante con estacionamiento, "
        "lugar cómodo para ir con mi abuelita."
    )

    lugares = obtener_lugares()

    if not lugares:
        st.warning("No se encontraron lugares registrados.")
        return

    consulta = st.text_input(
        "¿Qué lugar estás buscando?",
        placeholder="Ejemplo: Quiero un restaurante con rampas y estacionamiento en Tlalpan"
    )

    top_k = st.slider("Número de resultados", min_value=3, max_value=20, value=10)

    if consulta:
        resultados = recuperar_lugares(consulta, lugares, top_k=top_k)

        st.write(f"Resultados encontrados: **{len(resultados)}**")

        if resultados:
            for lugar in resultados:
                mostrar_lugar(lugar)
        else:
            st.info("No se encontraron resultados para tu consulta.")
    else:
        st.info("Escribe una consulta para obtener recomendaciones.")