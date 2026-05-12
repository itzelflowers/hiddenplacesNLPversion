import requests
import time
from utils.firebase import Firebase

# 1. Configuración Inicial
GOOGLE_API_KEY = "AIzaSyDHK32xHJ-8kRWAmPUlT6AhVVJCptAYDgM" # Asegúrate de que no tenga espacios al final
db = Firebase().getdb()

# Diccionario de alcaldías
alcaldias = {
    '09002': 'Azcapotzalco', '09003': 'Coyoacán', '09004': 'Cuajimalpa de Morelos',
    '09005': 'Gustavo A. Madero', '09006': 'Iztacalco', '09007': 'Iztapalapa',
    '09008': 'La Magdalena Contreras', '09009': 'Milpa Alta', '09010': 'Álvaro Obregón',
    '09011': 'Tláhuac', '09012': 'Tlalpan', '09013': 'Xochimilco',
    '09014': 'Benito Juárez', '09015': 'Cuauhtémoc', '09016': 'Miguel Hidalgo',
    '09017': 'Venustiano Carranza'
}

def poblar_cdmx_masivo():
    print("🚀 Iniciando poblamiento masivo (Filtro de Recreación y Cultura)...")
    
    # Palabras que queremos EVITAR (Ruido)
    lista_negra = [
        "ortopedia", "reparación", "venta de", "medical", "farmacia", 
        "clínica", "consultorio", "hospital", "biomedica", "sillas de ruedas"
    ]
    
    for cve, nombre_alcaldia in alcaldias.items():
        print(f"\n📍 Procesando: {nombre_alcaldia}...")
        
        # Refinamos la búsqueda para que nos de lugares de interés general
        query = f"restaurantes museos y parques accesibles con rampa en {nombre_alcaldia} CDMX"
        search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_API_KEY}&language=es"
        
        try:
            results = requests.get(search_url).json().get('results', [])
            
            puntos_guardados = 0
            for place in results:
                if puntos_guardados >= 3: # Seguimos con el límite de 3 por alcaldía
                    break
                
                nombre_lugar = place.get('name')
                
                # FILTRO DE SEGURIDAD: Si el nombre está en la lista negra, lo saltamos
                if any(negado in nombre_lugar.lower() for negado in lista_negra):
                    continue

                pid = place['place_id']
                
                # Detalles profundos
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=name,reviews,geometry,formatted_address,wheelchair_accessible_entrance&key={GOOGLE_API_KEY}&language=es"
                details = requests.get(details_url).json().get('result', {})
                
                opiniones = [rev['text'] for rev in details.get('reviews', [])]
                
                lugar_data = {
                    "Place": details.get('name'),
                    "Location": nombre_alcaldia,
                    "x": str(details['geometry']['location']['lat']),
                    "y": str(details['geometry']['location']['lng']),
                    "bss_type": "Recreación/Cultura",
                    "sillas_ruedas": "Sí" if details.get('wheelchair_accessible_entrance') else "No",
                    "estacionamiento": "Sí" if "estacionamiento" in str(opiniones).lower() else "No",
                    "rampas": "Sí" if "rampa" in str(opiniones).lower() else "No",
                    "elevadores": "Sí" if "elevador" in str(opiniones).lower() else "No",
                    "asistencia": "Sí",
                    "owner": "GOOGLE_SYSTEM",
                    "opiniones_brutas": opiniones,
                    "resumen_nlp": "" 
                }
                
                # Guardamos en Firebase (reemplazando puntos por guiones para evitar errores de ruta en Firebase)
                db_name = details.get('name').replace('.', '').replace('#', '').replace('$', '').replace('[', '').replace(']', '')
                db.child("Lugares").child(db_name).set(lugar_data)
                
                print(f"   ✅ Guardado: {nombre_lugar}")
                puntos_guardados += 1
                
            time.sleep(1) # Pausa para evitar bloqueos
            
        except Exception as e:
            print(f"   ❌ Error en {nombre_alcaldia}: {e}")

if __name__ == "__main__":
    poblar_cdmx_masivo()
    print("\n✨ ¡Base de datos limpia y poblada con éxito!")