import pandas as pd
import streamlit as st
from utils.firebase import Firebase

# Inicializamos la conexión
fb = Firebase()
db = fb.getdb()

@st.cache_data
def load_and_prep_data():
    """Trae los lugares de Firebase y los pone en un DataFrame"""
    # 1. Obtener datos del nodo 'lugares' que acabas de llenar con seed.py
    data = db.child("lugares").get().val()
    
    if not data:
        return pd.DataFrame() # Retorna vacío si no hay nada

    # 2. Convertir el diccionario de Firebase a una lista para Pandas
    lista_lugares = []
    for key, val in data.items():
        val['id'] = key # Guardamos el ID por si lo necesitamos
        lista_lugares.append(val)
    
    # 3. Crear el DataFrame
    df = pd.DataFrame(lista_lugares)
    
    # 4. Limpieza básica para NLP
    # Aseguramos que la descripción sea string y sin espacios locos
    df['descripcion'] = df['descripcion'].astype(str).str.strip()
    
    return df

def get_descriptions_list(df):
    """Extrae solo las descripciones para pasárselas a BERT"""
    return df['descripcion'].tolist()