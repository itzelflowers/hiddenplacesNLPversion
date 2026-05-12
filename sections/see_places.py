import sys
import os
import streamlit as st
from streamlit_folium import st_folium
import geopandas
import folium
from utils.firebase import Firebase

# 1. AJUSTE DE RUTAS (Para que encuentre 'utils' y 'CDMX' desde 'sections')
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

# 2. CONEXIÓN A FIREBASE
try:
    db = Firebase().getdb()
except Exception as e:
    st.error(f"Error al conectar con Firebase: {e}")

# 3. CARGA DEL SHAPEFILE (Carpeta CDMX)
@st.cache_data
def load_geodata():
    # root_path es la carpeta 'hackmexico2024'
    # Entramos a 'shapefiles', luego a la subcarpeta, y finalmente al archivo .shp
    ruta_shape = os.path.join(
        root_path, 
        'shapefiles', 
        'poligonos_alcaldias_cdmx', 
        'poligonos_alcaldias_cdmx.shp'
    )
    
    if not os.path.exists(ruta_shape):
        st.error(f"❌ No se encontró el archivo .shp en: {ruta_shape}")
        return None
        
    lineas = geopandas.read_file(ruta_shape)
    lineas['centroide'] = lineas.centroid
    return lineas

lineas_cdmx = load_geodata()

# Diccionario de Alcaldías para los Tooltips
alcaldias_dict = {
    '09002': 'Azcapotzalco', '09003': 'Coyoacán', '09004': 'Cuajimalpa de Morelos',
    '09005': 'Gustavo A. Madero', '09006': 'Iztacalco', '09007': 'Iztapalapa',
    '09008': 'La Magadalena Contreras', '09009': 'Milpa Alta', '09010': 'Álvaro Obregón',
    '09011': 'Tláhuac', '09012': 'Tlalpan', '09013': 'Xochimilco',
    '09014': 'Benito Juárez', '09015': 'Cuauhtémoc', '09016': 'Miguel Hidalgo',
    '09017': 'Venustiano Carranza'
}

# 4. FUNCIONES DEL MAPA
def init_map(center=(19.4325019109759, -99.1322510732777), zoom_start=11):
    return folium.Map(location=center, zoom_start=zoom_start, tiles="cartodbpositron")

def plot_polygons(folium_map):
    if lineas_cdmx is not None:
        for idx, row in lineas_cdmx.iterrows():
            cve = row.get('CVEGEO', '')
            nombre = alcaldias_dict.get(cve, "CDMX")
            
            folium.GeoJson(
                row.geometry,
                style_function=lambda x: {
                    'fillColor': '#FF0000', 
                    'color': '#000000', 
                    'weight': 1, 
                    'fillOpacity': 0.1
                },
                tooltip=nombre
            ).add_to(folium_map)
    return folium_map

# 5. APLICACIÓN PRINCIPAL
def app():
    st.title("🗺️ Algunos lugares escondidos...")
    st.write("Explora los rincones de la CDMX que ya están listos para recibirte.")
    
    m = init_map()
    m = plot_polygons(m)
    
    # Traer todos los lugares de Firebase
    lugares_data = db.child('Lugares').get().val()
    
    if lugares_data:
        for nombre_lugar, info in lugares_data.items():
            owner = info.get('owner')
            
            # Verificamos si el usuario está loggeado en la sesión
            user_id = st.session_state.get('ID', None)
            
            # FILTRO: Mostramos si es del usuario O si es de Google
            if user_id == owner or owner == "GOOGLE_SYSTEM":
                lat = info.get('x')
                lng = info.get('y')
                
                if lat and lng:
                    # Color diferente: Azul para usuario, Púrpura para Google
                    icon_color = "blue" if owner != "GOOGLE_SYSTEM" else "purple"
                    
                    folium.Marker(
                        [float(lat), float(lng)],
                        tooltip=nombre_lugar,
                        icon=folium.Icon(color=icon_color, icon="info-sign")
                    ).add_to(m)

    # Renderizar el mapa en Streamlit
    # Agregamos use_container_width para que se ajuste bien a la pantalla azul
    map_output = st_folium(m, width=700, height=500)
    
    # 6. DETALLES DEL LUGAR SELECCIONADO
    selected_name = map_output.get('last_object_clicked_tooltip')
    
    if selected_name:
        st.markdown("---")
        st.subheader(f"📍 {selected_name}")
        
        # Consultar la data del lugar seleccionado
        detalle = db.child('Lugares').child(selected_name).get().val()
        
        if detalle:
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**Tipo:** {detalle.get('bss_type', 'N/A')}")
                st.write(f"🏠 **Alcaldía:** {detalle.get('Location', 'N/A')}")
                st.write(f"♿ **Acceso Silla:** {detalle.get('sillas_ruedas', 'No info')}")
            
            with c2:
                st.write(f"🛤️ **Rampas:** {detalle.get('rampas', 'No info')}")
                st.write(f"🛗 **Elevadores:** {detalle.get('elevadores', 'No info')}")
                st.write(f"🤝 **Asistencia:** {detalle.get('asistencia', 'No info')}")

            st.markdown("#### 🧠 Análisis de Inteligencia Artificial (NLP)")
            resumen = detalle.get('resumen_nlp', "")
            
            if resumen and resumen.strip() != "":
                st.success(resumen)
            else:
                st.warning("El algoritmo de NLP está procesando las reseñas actuales...")
    else:
        st.info("Haz clic en un marcador del mapa para ver el análisis de accesibilidad.")

if __name__ == "__main__":
    # Si corres este archivo solo para pruebas
    if 'ID' not in st.session_state:
        st.session_state.ID = "test_user" # Para que no truene si pruebas local
    app()