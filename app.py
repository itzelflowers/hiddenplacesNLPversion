import streamlit as st

st.set_page_config(
    page_title="Hidden Places | Home",
    page_icon="🗺️",
    initial_sidebar_state="expanded",
)

from sections import login, maps, home
from utils.firebase import Firebase

def bussines_register():
    st.title("Registro de Empresas")
    email = st.text_input('Correo Electrónico')
    password = st.text_input('Contraseña', type='password')
    name = st.text_input('Nombre Empresa')
    bss_type = st.selectbox('Tipo de Empresa', ['Comida', 'Cultura', 'Entretenimiento'])
    submit = st.button("Crear Empresa")
    if submit:           
        db = Firebase().getdb()
        auth = Firebase().getauth()
        user = auth.create_user_with_email_and_password(email, password)
        db.child(user['localId']).child('ID').set(user['localId'])
        db.child(user['localId']).child('email').set(email)
        db.child(user['localId']).child('password').set(password)
        db.child(user['localId']).child('user_type').set('bussines')
        db.child(user['localId']).child('name').set(name)
        db.child(user['localId']).child('bss_type').set(bss_type)
        st.success('La cuenta ha sido creada correctamente.')
        st.balloons()

def user_register():
    st.title("Registro de Usuarios")
    email = st.text_input('Correo Electrónico')
    password = st.text_input('Contraseña', type='password')
    name = st.text_input('Nombre')
    last_name = st.text_input("Apellidos")
    submit = st.button("Crear Usuario")
    if submit:           
        db = Firebase().getdb()
        auth = Firebase().getauth()
        user = auth.create_user_with_email_and_password(email, password)
        db.child(user['localId']).child('ID').set(user['localId'])
        db.child(user['localId']).child('email').set(email)
        db.child(user['localId']).child('password').set(password)
        db.child(user['localId']).child('user_type').set('client')
        db.child(user['localId']).child('name').set(name)
        db.child(user['localId']).child('last_name').set(last_name)
        st.success('La cuenta ha sido creada correctamente.')
        st.balloons()

def register():
    st.title("Registrate")
    selected_option = st.radio("¿Qué tipo de usuario eres?", ("Cliente", "Empresa"))
    if selected_option == 'Cliente':
        user_register()
    else:
        bussines_register()

login.app()

if st.session_state['user_type'] != '':
    pass
else:
    if "selection" not in st.session_state:
        home.app()
        st.subheader("¿Quieres explorar más lugares?")
        if st.button("Registrar"):
            st.session_state.selection = "REGISTRAR"
    elif st.session_state.selection == "REGISTRAR":
        register()
    else:
        home.app()
        st.subheader("¿Quieres explorar más lugares?")
        if st.button("Registrar"):
            st.session_state.selection = "REGISTRAR"