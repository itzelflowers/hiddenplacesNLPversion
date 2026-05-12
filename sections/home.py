import streamlit as st
import os
import sys

# Parche para que encuentre 'maps' y 'utils' sin importar desde dónde ejecutas
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# Importamos maps de forma perezosa para evitar el lag inicial
from sections import maps

def app():
    # --- LOGICA DE ESTADO ---
    # Si el usuario NO ha iniciado sesión, mostramos tu diseño original
    if not st.session_state.get('signout', False):
        
        st.title("Bienvenidos a Hidden Places", anchor=None)
        
        # Tus estilos originales
        st.markdown("""
            <style>
                .slogan { padding-left: 1em; }
                .map-container { padding: 2em 0em; }
                .qual-list { padding-right: 1em; }
            </style>
        """, unsafe_allow_html=True)
        
        # Slogan y descripción
        st.write('<div class="slogan"><h2>Explora sin Límites 🌍</h2></div>', unsafe_allow_html=True)
        st.markdown("""
        **Hidden Places** es tu guía para un turismo accesible en la CDMX. Nos comprometemos a que personas con discapacidad motriz y adultos mayores disfruten de cada rincón con total libertad. 

        Con **facilidades accesibles**, comunidad interactiva y beneficios exclusivos, cada visita se convierte en una experiencia inolvidable.

        Las empresas tienen una nueva ventana al mundo del turismo inclusivo, descubriendo oportunidades para todos.
        """)
        
        # Lista de cualidades y el mapa
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="qual-list"><h3>Cualidades de Hidden Places:</h3>', unsafe_allow_html=True)
            st.markdown("""
            - Accesibilidad garantizada 🚪
            - Comunidad activa 👥
            - Beneficios y descuentos 🎁
            - Compromiso con la inclusión 💖
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            # Aquí se carga el mapa rojo de alcaldías
            maps.app()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Texto debajo del mapa
        st.write("""
        Descubre los destinos turísticos más acogedores para todos, con la seguridad y el confort que mereces.
        Únete a Hidden Places y sé parte de la aventura. ¡Tu próxima gran experiencia comienza aquí!
        """)

        st.write('<br>', unsafe_allow_html=True)
        
        if st.button('Descubre más sobre Hidden Places'):
            st.info("¡Inicia sesión en la barra lateral para explorar el mapa interactivo completo!")

    # --- SI YA INICIÓ SESIÓN ---
    # Cambiamos la vista a la página de inicio del usuario
    else:
        from sections import user_home
        user_home.app()
