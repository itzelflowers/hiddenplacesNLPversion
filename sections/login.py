# Importar librerías necesarias.
import streamlit as st
from utils.firebase_utils import login_session
from utils.firebase import Firebase
from sections import register_places, home, see_places, user_home, recomendaciones, sectores, visited_places
from streamlit_lottie import st_lottie
import json
from sections.membership import display_rewards_table

db = Firebase().getdb()

def obtener_datos_usuario():
    nombre = db.child(st.session_state['ID']).child('name').get().val()
    apellido = db.child(st.session_state['ID']).child('last_name').get().val()
    correo = db.child(st.session_state['ID']).child('email').get().val()
    return {"Nombre": nombre, "Correo Electrónico": correo, "Apellido": apellido}

def load_lottiefile(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

def app():
    if 'ID' not in st.session_state: st.session_state['ID'] = ''
    if 'user_type' not in st.session_state: st.session_state['user_type'] = ''
    if 'name' not in st.session_state: st.session_state['name'] = ''
    if 'bss_type' not in st.session_state: st.session_state['bss_type'] = ''
    if 'last_name' not in st.session_state: st.session_state['last_name'] = ''
    if 'signedout' not in st.session_state: st.session_state['signedout'] = False
    if 'signout' not in st.session_state: st.session_state['signout'] = False

    def logout_session():
        st.session_state['signedout'] = False
        st.session_state['signout'] = False
        st.session_state['ID'] = ''
        st.session_state['name'] = ''
        st.session_state['last_name'] = ''
        st.session_state['bss_type'] = ''
        st.session_state['user_type'] = ''

    st.markdown("""
        <style>
        div.stButton > button:first-child { background-color: #f97316; color: white; border: none; }
        div.stButton > button:hover { background-color: #fb923c; border: none; }
        </style>
    """, unsafe_allow_html=True)

    # --- SIN SESIÓN ---
    if not st.session_state['signedout']:
        st.sidebar.image('./img/logoconnombre.png', use_column_width=True, width=180)
        st.sidebar.title("Inicio de Sesión")
        st.sidebar.write("Inicia Sesión para ver más características")
        text_email = st.sidebar.text_input('Correo Electrónico', key='email')
        text_password = st.sidebar.text_input('Contraseña', type='password', key='password')
        st.sidebar.button("Iniciar Sesión", on_click=login_session, args=(text_email, text_password))

        # --- REGISTRO ---
        st.sidebar.markdown("---")
        with st.sidebar.expander("✨ ¿Eres nuevo? Regístrate aquí"):
            st.text_input("Nombre(s)", key="reg_n")
            st.text_input("Apellidos", key="reg_a")
            st.text_input("Correo", key="reg_e")
            st.text_input("Contraseña", type="password", key="reg_p")
            st.selectbox("Tipo de cuenta", ["Cliente", "Empresa"], key="reg_tipo")

            if st.button("Crear Cuenta", key="btn_crear_cuenta"):
                nombre   = st.session_state.get("reg_n", "")
                apellido = st.session_state.get("reg_a", "")
                email    = st.session_state.get("reg_e", "")
                password = st.session_state.get("reg_p", "")
                tipo     = st.session_state.get("reg_tipo", "Cliente")

                if nombre and email and password:
                    try:
                        auth = Firebase().getauth()
                        user = auth.create_user_with_email_and_password(email, password)
                        uid = user['localId']
                        user_role = 'bussines' if tipo == "Empresa" else 'client'
                        db.child(uid).child('ID').set(uid)
                        db.child(uid).child('email').set(email)
                        db.child(uid).child('password').set(password)
                        db.child(uid).child('user_type').set(user_role)
                        db.child(uid).child('name').set(nombre)
                        db.child(uid).child('last_name').set(apellido)
                        if user_role == 'bussines':
                            db.child(uid).child('bss_type').set('Por definir')
                        st.success("¡Cuenta creada! Ya puedes iniciar sesión.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("⚠️ Nombre, correo y contraseña son obligatorios.")

        lottie_intro = load_lottiefile("./img/similo3.json")
        with st.sidebar:
            st_lottie(lottie_intro)

 # --- CON SESIÓN ---
    if st.session_state['signout']:
        lottie_intro = load_lottiefile("./img/similo3.json")
        st.sidebar.image('./img/logoconnombre.png', use_column_width=True, width=180)
        st.sidebar.title("Bienvenido")

        if st.session_state['user_type'] == 'bussines':
            try:
                if not st.session_state['name']:
                    st.session_state['name'] = db.child(st.session_state.ID).child('name').get().val()
                    st.session_state['bss_type'] = db.child(st.session_state.ID).child('bss_type').get().val()
            except Exception:
                st.rerun()

            st.sidebar.subheader(f'{st.session_state["name"]}')
            st.sidebar.markdown(f'**Giro de la empresa**: {st.session_state["bss_type"]}')

            if st.sidebar.button("Registrar Lugar"): st.session_state.selection = "LUGARES"
            if st.sidebar.button("Ver Lugares"): st.session_state.selection = "VER_LUGARES"

            if "selection" not in st.session_state:
                register_places.app()
            elif st.session_state.selection == "VER_LUGARES":
                see_places.app()
            else:
                register_places.app()

        else:
            try:
                if not st.session_state['name']:
                    st.session_state['name'] = db.child(st.session_state.ID).child('name').get().val()
                    st.session_state['last_name'] = db.child(st.session_state.ID).child('last_name').get().val()
            except Exception:
                st.rerun()

            st.sidebar.subheader(f'{st.session_state["name"]} {st.session_state["last_name"]}')

            if st.sidebar.button("Inicio"): st.session_state.selection = "INICIO"
            if st.sidebar.button("Perfil"): st.session_state.selection = "PERFIL"
            if st.sidebar.button("Sectores"): st.session_state.selection = "SECTORES"
            if st.sidebar.button("Recompensas"): st.session_state.selection = "RECOMPENSAS"
            if st.sidebar.button("Recomendaciones"): st.session_state.selection = "RECOMENDACIONES"
            if st.sidebar.button("Lugares Visitados"): st.session_state.selection = "VISITED"

            if "selection" not in st.session_state:
                user_home.app()
            elif st.session_state.selection == "INICIO":
                user_home.app()
            elif st.session_state.selection == "RECOMENDACIONES":
                recomendaciones.app()
            elif st.session_state.selection == "SECTORES":
                sectores.app()
            elif st.session_state.selection == "PERFIL":
                datos_usuario = obtener_datos_usuario()
                st.title("Datos del Usuario 📄")
                st.write(f"**Nombre:** {datos_usuario['Nombre']} 👤")
                st.write(f"**Apellido:** {datos_usuario['Apellido']} 👥")
                st.write(f"**Correo Electrónico:** {datos_usuario['Correo Electrónico']} 📧")
                st.write(f"**Tipo de Usuario:** {st.session_state['user_type']} 🛂")
                st.write(f"**ID:** {st.session_state['ID']} 🔖")
                st.write("Usuario desde: 14 de Abril de 2024 📅")
                lottie_perfil = load_lottiefile("./img/place2.json")
                st_lottie(lottie_perfil)
            elif st.session_state.selection == "RECOMPENSAS":
                display_rewards_table()
            elif st.session_state.selection == "VISITED":
                visited_places.app()
            else:
                user_home.app()

        st.sidebar.button("Cerrar Sesión", on_click=logout_session)
        with st.sidebar:
            st_lottie(lottie_intro)
