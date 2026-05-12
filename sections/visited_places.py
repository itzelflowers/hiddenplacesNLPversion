# Importar librerías necesarias.
import streamlit as st
from streamlit_folium import st_folium
import geopandas
import folium
from utils.firebase import Firebase
import random

db = Firebase().getdb()

# Shapefile CDMX.
lineas_cdmx = geopandas.read_file(('./shapefiles/poligonos_alcaldias_cdmx/poligonos_alcaldias_cdmx.shp'))
lineas_cdmx['centroide'] = lineas_cdmx.centroid

# Diccionario.
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

def init_map(center=(19.4325019109759, -99.1322510732777), zoom_start=10, map_type="cartodbpositron"):
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type)

def plot_map(folium_map):
    for idx, row in lineas_cdmx.iterrows():
        folium.GeoJson(row.geometry,
                       style_function=lambda x: {'fillColor': '#FF0000', 'color': '#000000', 'weight': 1.5, 'fillOpacity': 0.5},
                       tooltip=alcaldias[row['CVEGEO']]).add_to(folium_map)
    return folium_map

def app():
    st.title("Tus lugares visitados")
    m = init_map()
    m = plot_map(m)

    # Obtener lugares con fix de Firebase
    lugares_raw = db.child('Lugares').get()
    lugares_keys = []

    if lugares_raw.each():
        for lugar in lugares_raw.each():
            nombre = lugar.key()
            datos = lugar.val()
            x = datos.get('x')
            y = datos.get('y')
            if x is not None and y is not None:
                lugares_keys.append(nombre)
                folium.Marker([float(x), float(y)], tooltip=nombre).add_to(m)

    # Mostrar solo 10 aleatorios
    random.shuffle(lugares_keys)
    lugares_keys = lugares_keys[:10]

    level1_map_data = st_folium(m)
    st.session_state.selected_id = level1_map_data['last_object_clicked_tooltip']

    if st.session_state.selected_id is not None:
        nombre = st.session_state.selected_id
        st.subheader(nombre)

        datos = db.child('Lugares').child(nombre).get().val()

        if datos:
            st.write(f'Alcaldía: {datos.get("Location", "N/A")}')
            st.write(f'Tipo de negocio: {datos.get("bss_type", "N/A")}')
            st.write(f'Asistencia Personal: {datos.get("asistencia", "N/A")}')
            st.write(f'Elevadores: {datos.get("elevadores", "N/A")}')
            st.write(f'Estacionamiento: {datos.get("estacionamiento", "N/A")}')
            st.write(f'Rampas: {datos.get("rampas", "N/A")}')
            st.write(f'Sillas de ruedas: {datos.get("sillas_ruedas", "N/A")}')

            # --- SECCIÓN DE COMENTARIOS ---
            st.markdown("---")
            st.subheader("💬 Comentarios de usuarios")

            # Mostrar comentarios existentes
            comentarios = datos.get("comentarios_usuarios", {})
            if comentarios:
                for uid, comentario in comentarios.items():
                    st.markdown(f"👤 **{comentario.get('nombre', 'Usuario')}**: {comentario.get('texto', '')}")
            else:
                st.write("Sé el primero en comentar este lugar.")

            # Formulario para agregar comentario
            st.markdown("---")
            st.subheader("✍️ Deja tu comentario")
            st.text_area("¿Cómo fue tu experiencia?", key="nuevo_comentario")

            if st.button("Publicar comentario", key="btn_comentario"):
             texto = st.session_state.get("nuevo_comentario", "")
             if texto:
                nombre_usuario = st.session_state.get("name", "Usuario")
        # Obtener comentarios existentes
                opiniones_actuales = datos.get("opiniones_brutas", {})
        
        # Calcular el siguiente índice
                if opiniones_actuales:
                 siguiente_index = max([int(k) for k in opiniones_actuales.keys()]) + 1
                else:
                 siguiente_index = 0

        # Guardar en opiniones_brutas con el siguiente índice
                 db.child('Lugares').child(nombre).child('opiniones_brutas').child(str(siguiente_index)).set(
                 f"{nombre_usuario}: {texto}"
                 )
        
        # Limpiar resumen_nlp para que se regenere con la nueva opinión
                 db.child('Lugares').child(nombre).child('resumen_nlp').set("")
        
                 st.success("¡Comentario publicado!")
                st.rerun()
             else:
              st.warning("Escribe algo antes de publicar.")