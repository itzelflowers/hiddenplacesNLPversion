import streamlit as st
from streamlit_folium import st_folium
import geopandas
import folium
from utils.firebase import Firebase
from transformers import pipeline

db = Firebase().getdb()

# Shapefile CDMX.
lineas_cdmx = geopandas.read_file(('./shapefiles/poligonos_alcaldias_cdmx/poligonos_alcaldias_cdmx.shp'))
lineas_cdmx['centroide'] = lineas_cdmx.centroid

alcaldias = {
    '09002': 'Azcapotzalco',
    '09003': 'Coyoacán',
    '09004': 'Cuajimalpa de Morelos',
    '09005': 'Gustavo A. Madero',
    '09006': 'Iztacalco',
    '09007': 'Iztapalapa',
    '09008': 'La Magadalena Contreras',
    '09009': 'Milpa Alta',
    '09010': 'Álvaro Obregón',
    '09011': 'Tláhuac',
    '09012': 'Tlalpan',
    '09013': 'Xochimilco',
    '09014': 'Benito Juárez',
    '09015': 'Cuauhtémoc',
    '09016': 'Miguel Hidalgo',
    '09017': 'Venustiano Carranza'
}

@st.cache_resource
def cargar_modelo():
    try:
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception:
        return pipeline("text2text-generation", model="t5-small")

def generar_resumen(opiniones_brutas):
    if not opiniones_brutas:
        return "Sin opiniones disponibles."

    if isinstance(opiniones_brutas, list):
        texto = " ".join([op for op in opiniones_brutas if op])
    elif isinstance(opiniones_brutas, dict):
        texto = " ".join(opiniones_brutas.values())
    else:
        return "Sin opiniones disponibles."

    texto = texto[:1024]
    summarizer = cargar_modelo()
    resumen = summarizer(texto, max_length=130, min_length=30, do_sample=False)
    
    # Manejar ambos formatos de respuesta
    resultado = resumen[0]
    return resultado.get('summary_text') or resultado.get('generated_text', 'Sin resumen disponible.')

def init_map(center=(19.4325019109759, -99.1322510732777), zoom_start=10, map_type="cartodbpositron"):
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type)

def plot_map(folium_map):
    for idx, row in lineas_cdmx.iterrows():
        folium.GeoJson(row.geometry,
                       style_function=lambda x: {'fillColor': '#FF69B4', 'color': '#000000', 'weight': 1.5, 'fillOpacity': 0.3},
                       tooltip=alcaldias[row['CVEGEO']]).add_to(folium_map)
    return folium_map

def app():
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
            # Convertir a dict si Firebase devuelve lista
            if isinstance(datos, list):
                datos = {str(i): v for i, v in enumerate(datos) if v is not None}

            # --- NOMBRE DEL LUGAR ---
            st.markdown(f"## 📍 {nombre}")
            st.markdown("---")

            # --- TARJETA DE TIPO ---
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

            resumen_guardado = datos.get("resumen_nlp", "")

            if resumen_guardado:
                st.info(resumen_guardado)
            elif opiniones is not None:
                with st.spinner("El algoritmo de NLP está procesando las reseñas actuales..."):
                    resumen = generar_resumen(opiniones)
                    db.child('Lugares').child(nombre).child('resumen_nlp').set(resumen)
                    st.info(resumen)
            else:
                st.info("No hay reseñas disponibles para este lugar.")