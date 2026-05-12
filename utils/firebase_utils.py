from utils.firebase import Firebase
import streamlit as st

def login_session(email, password):
    try:
        db = Firebase().getdb()
        auth = Firebase().getauth()
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state['signedout'] = True
        st.session_state['signout'] = True
        # Usar localId directamente en lugar de leerlo de la DB
        st.session_state['ID'] = user['localId']
        st.session_state['user_type'] = db.child(user['localId']).child('user_type').get().val()
        st.success("Inicio de Sesión Exitoso")
    except Exception as e:
        st.warning('No es posible Iniciar Sesión')