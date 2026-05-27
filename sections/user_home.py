import streamlit as st
from streamlit_folium import st_folium
import geopandas
import folium
from utils.firebase import Firebase
from transformers import pipeline
from utils.preprocesamiento import preprocesar_opiniones

db = Firebase().getdb()

lineas_cdmx = geopandas.read_file(('./shapefiles/poligonos_alcaldias_cdmx/poligonos_alcaldias_cdmx.shp'))
lineas_cdmx['centroide'] = lineas_cdmx.centroid

alcaldias = {
    '09002': 'Azcapotzalco', '09003': 'Coyoacán', '09004': 'Cuajimalpa de Morelos',
    '09005': 'Gustavo A. Madero', '09006': 'Iztacalco', '09007': 'Iztapalapa',
    '09008': 'La Magadalena Contreras', '09009': 'Milpa Alta', '09010': 'Álvaro Obregón',
    '09011': 'Tláhuac', '09012': 'Tlalpan', '09013': 'Xochimilco',
    '09014': 'Benito Juárez', '09015': 'Cuauhtémoc', '09016': 'Miguel Hidalgo',
    '09017': 'Venustiano Carranza'
}

@st.cache_resource
def cargar_modelo():
    try:
        return pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    except Exception:
        return pipeline("text-generation", model="gpt2")

def generar_resumen(opiniones_brutas):
    if not opiniones_brutas:
        return "Sin opiniones disponibles."

    if isinstance(opiniones_brutas, list):
        texto = " ".join([str(op) for op in opiniones_brutas if op])
    elif isinstance(opiniones_brutas, dict):
        texto = " ".join([str(op) for op in opiniones_brutas.values() if op])
    else:
        texto = str(opiniones_brutas)

    texto = texto.strip()
    if not texto:
        return "Sin opiniones disponibles."

    # Limitar a 300 palabras
    palabras = texto.split()[:300]
    texto = " ".join(palabras)

    summarizer = cargar_modelo()
    try:
        resumen = summarizer(texto, max_length=150, min_length=40, do_sample=False, truncation=True)
        resultado = resumen[0]
        return resultado.get("summary_text") or resultado.get("generated_text", "Sin resumen disponible.")
    except Exception as e:
        return f"No se pudo generar el resumen: {e}"

def init_map(center=(19.4325019109759, -99.1322510732777), zoom_start=10, map_type="cartodbpositron"):
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type)

def plot_map(folium_map):
    for idx, row in lineas_cdmx.iterrows():
        folium.GeoJson(row.geometry,
                       style_function=lambda x: {'fillColor': '#FF69B4', 'color': '#000000', 'weight': 1.5, 'fillOpacity': 0.3},
                       tooltip=alcaldias[row['CVEGEO']]).add_to(folium_map)
    return folium_map

def app():
    # --- TÍTULO ---
    st.title("🗺️ Explora todos los lugares")
    st.markdown("<p style='color:gray;'>Selecciona un marcador para ver los detalles de accesibilidad.</p>", unsafe_allow_html=True)

    m = init_map()
    m = plot_map(m)

    lugares_raw = db.child('Lugares').get()
    if lugares_raw.each():
        for lugar in lugares_raw.each():
            datos_lugar = lugar.val()
            x = datos_lugar.get('x')
            y = datos_lugar.get('y')
            if x is not None and y is not None:
                folium.Marker(
                    [float(x), float(y)],
                    tooltip=lugar.key(),
                    icon=folium.Icon(color='purple', icon='info-sign')
                ).add_to(m)

    level1_map_data = st_folium(m, width=700, height=500)
    st.session_state.selected_id = level1_map_data['last_object_clicked_tooltip']

    if st.session_state.selected_id is not None:
        nombre = st.session_state.selected_id
        datos = db.child('Lugares').child(nombre).get().val()

        if datos:
            if isinstance(datos, list):
                datos = {str(i): v for i, v in enumerate(datos) if v is not None}

            st.markdown(f"## 📍 {nombre}")
            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                bss_type = datos.get("bss_type", "N/A")
                st.markdown(f"""
                    <div style='background-color:#1e3a5f; padding:12px; border-radius:8px; color:#4fc3f7;'>
                        <b>Tipo:</b> {bss_type}
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"🏠 **Alcaldía:** {datos.get('Location', 'N/A')}")
                st.markdown(f"♿ **Acceso Silla:** {datos.get('sillas_ruedas', 'N/A')}")
            with col2:
                st.markdown(f"🚧 **Rampas:** {datos.get('rampas', 'N/A')}")
                st.markdown(f"🛗 **Elevadores:** {datos.get('elevadores', 'N/A')}")
                st.markdown(f"🤝 **Asistencia:** {datos.get('asistencia', 'N/A')}")

            # --- OPINIONES ---
            st.markdown("---")
            st.markdown("## 💬 Opiniones de visitantes")
            opiniones = datos.get("opiniones_brutas", None)

            if opiniones:
                if isinstance(opiniones, list):
                    lista_opiniones = [op for op in opiniones if op]
                elif isinstance(opiniones, dict):
                    lista_opiniones = list(opiniones.values())
                else:
                    lista_opiniones = []

                for opinion in lista_opiniones:
                    st.markdown(f"""
                        <div style='background-color:#1a2a3a; padding:10px; border-radius:8px; margin-bottom:8px; color:#ccc;'>
                            ⭐ <i>{opinion}</i>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No hay opiniones disponibles para este lugar.")

            # --- SECCIÓN NLP ---
            st.markdown("---")
            st.markdown("## 🧠 Análisis de Inteligencia Artificial (NLP)")

            bss_type = datos.get("bss_type", "")

            if bss_type == "Salud":
                st.markdown("### ♿ Análisis de Accesibilidad")
                CATEGORIAS_ACCESIBILIDAD = {
                    "rampas": ["rampa", "rampas", "acceso", "entrada accesible", "desnivel", "escalón", "escalones"],
                    "elevadores": ["elevador", "elevadores", "ascensor", "lift", "sube", "subir", "piso", "nivel"],
                    "sillas_ruedas": ["silla de ruedas", "silla ruedas", "wheelchair", "movilidad reducida", "discapacidad", "accesible"],
                    "estacionamiento": ["estacionamiento accesible", "cajón", "espacio discapacitados", "estacionamiento", "parking"],
                    "asistencia": ["ayuda", "asistencia", "apoyo", "personal", "amable", "ayudaron", "atención", "servicio"]
                }
                if opiniones:
                    texto = preprocesar_opiniones(opiniones)
                    col1, col2 = st.columns(2)
                    emojis = {"rampas": "🚧", "elevadores": "🛗", "sillas_ruedas": "♿", "estacionamiento": "🅿️", "asistencia": "🤝"}
                    for i, (categoria, palabras) in enumerate(CATEGORIAS_ACCESIBILIDAD.items()):
                        menciones = [p for p in palabras if p in texto]
                        score = round((len(menciones) / len(palabras)) * 10, 1)
                        col = col1 if i % 2 == 0 else col2
                        with col:
                            st.metric(label=f"{emojis[categoria]} {categoria.replace('_', ' ').title()}", value=f"{score}/10")
                            if menciones:
                                st.caption(f"Menciones: {', '.join(menciones)}")
                else:
                    st.info("No hay opiniones disponibles para analizar.")

            else:
                st.markdown("### 🌟 Resumen de experiencia")
                ASPECTOS_GENERALES = {
                    "experiencia": ["increíble", "recomendable", "vale la pena", "bonito", "hermoso", "excelente", "maravilloso", "espectacular"],
                    "servicio": ["atención", "amable", "servicio", "trato", "personal", "amabilidad", "atentos"],
                    "accesibilidad": ["rampa", "elevador", "silla", "accesible", "discapacidad", "movilidad"],
                    "precio": ["precio", "caro", "barato", "económico", "cobran", "costo"],
                    "ubicación": ["ubicación", "llegar", "transporte", "estacionamiento", "céntrico"]
                }
                if opiniones:
                    texto = preprocesar_opiniones(opiniones)
                    aspectos_encontrados = []
                    for aspecto, palabras in ASPECTOS_GENERALES.items():
                        menciones = [p for p in palabras if p in texto]
                        if menciones:
                            aspectos_encontrados.append(f"**{aspecto.title()}**: {', '.join(menciones)}")
                    if aspectos_encontrados:
                        for aspecto in aspectos_encontrados:
                            st.markdown(f"✅ {aspecto}")
                    else:
                        st.info("No se encontraron aspectos relevantes en las opiniones.")
                else:
                    st.info("No hay opiniones disponibles para este lugar.")

            # --- RESUMEN DISTILBART ---
            st.markdown("---")
            st.markdown("### 📝 Resumen general")

            resumen_guardado = datos.get("resumen_nlp", "")

            if resumen_guardado:
                # Ya existe — mostrar directo sin regenerar
                st.info(resumen_guardado)
            elif opiniones:
                # Generar, guardar en Firebase y mostrar
                with st.spinner("Generando resumen automático con IA..."):
                    resumen = generar_resumen(opiniones)
                    db.child('Lugares').child(nombre).child('resumen_nlp').set(resumen)
                    st.info(resumen)
            else:
                st.info("Sin resumen disponible.")