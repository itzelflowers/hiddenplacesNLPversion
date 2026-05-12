import streamlit as st
from streamlit_folium import st_folium
import geopandas
import folium
import os
from utils.firebase import Firebase

# 1. RUTAS Y CONEXIÓN
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
ruta_shape = os.path.join(root_path, 'shapefiles', 'poligonos_alcaldias_cdmx', 'poligonos_alcaldias_cdmx.shp')

db = Firebase().getdb()

# 2. CARGA DE SHAPEFILE
@st.cache_data
def load_geodata():
    if os.path.exists(ruta_shape):
        return geopandas.read_file(ruta_shape)
    return None

lineas_cdmx = load_geodata()

# 3. DICCIONARIO DE ALCALDÍAS
alcaldias_dict = {
    '09002': 'Azcapotzalco', '09003': 'Coyoacán', '09004': 'Cuajimalpa de Morelos',
    '09005': 'Gustavo A. Madero', '09006': 'Iztacalco', '09007': 'Iztapalapa',
    '09008': 'La Magadalena Contreras', '09009': 'Milpa Alta', '09010': 'Álvaro Obregón',
    '09011': 'Tláhuac', '09012': 'Tlalpan', '09013': 'Xochimilco',
    '09014': 'Benito Juárez', '09015': 'Cuauhtémoc', '09016': 'Miguel Hidalgo',
    '09017': 'Venustiano Carranza'
}

def app():
    # Inicializar mapa
    m = folium.Map(location=[19.4325, -99.1332], zoom_start=11, tiles="cartodbpositron")
    
    # Dibujar Polígonos
    if lineas_cdmx is not None:
        for idx, row in lineas_cdmx.iterrows():
            cve = row.get('CVEGEO', '')
            nombre = alcaldias_dict.get(cve, "CDMX")
            folium.GeoJson(
                row.geometry,
                style_function=lambda x: {'fillColor': '#FF0000', 'color': 'black', 'weight': 1, 'fillOpacity': 0.1},
                tooltip=nombre
            ).add_to(m)

    # 4. TRAER MARCADORES (Usando x e y como en tu código)
    try:
        lugares_data = db.child('Lugares').get().val()
        if lugares_data:
            for nombre_lugar, info in lugares_data.items():
                lat = info.get('x') # <-- Importante: tu Firebase usa 'x'
                lng = info.get('y') # <-- Importante: tu Firebase usa 'y'
                
                if lat and lng:
                    folium.Marker(
                        location=[float(lat), float(lng)],
                        tooltip=nombre_lugar,
                        # Solo el nombre en el popup para la portada
                        popup=folium.Popup(f"<b>{nombre_lugar}</b>", max_width=200),
                        icon=folium.Icon(color="purple", icon="info-sign")
                    ).add_to(m)
    except Exception as e:
        pass

    # Renderizar
    st_folium(m, width=700, height=500, key="mapa_home", returned_objects=[])