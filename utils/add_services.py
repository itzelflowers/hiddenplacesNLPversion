import requests
import time
from utils.firebase import Firebase

GOOGLE_API_KEY = "AIzaSyDHK32xHJ-8kRWAmPUlT6AhVVJCptAYDgM"
db = Firebase().getdb()

alcaldias = {
    '09002': 'Azcapotzalco', '09003': 'Coyoacán', '09004': 'Cuajimalpa de Morelos',
    '09005': 'Gustavo A. Madero', '09006': 'Iztacalco', '09007': 'Iztapalapa',
    '09008': 'La Magdalena Contreras', '09009': 'Milpa Alta', '09010': 'Álvaro Obregón',
    '09011': 'Tláhuac', '09012': 'Tlalpan', '09013': 'Xochimilco',
    '09014': 'Benito Juárez', '09015': 'Cuauhtémoc', '09016': 'Miguel Hidalgo',
    '09017': 'Venustiano Carranza'
}

def agregar_servicios_tecnicos():
    print("🛠️ Agregando servicios de soporte y ortopedias...")
    
    for cve, nombre_alcaldia in alcaldias.items():
        print(f"\n📍 Buscando servicios en: {nombre_alcaldia}...")
        
        # Query específica para lo que borramos
        query = f"venta y reparacion de sillas de ruedas ortopedia en {nombre_alcaldia} CDMX"
        search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_API_KEY}&language=es"
        
        try:
            results = requests.get(search_url).json().get('results', [])
            
            # Solo agregamos 1 o 2 por alcaldía para no saturar
            for place in results[:2]:
                pid = place['place_id']
                
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=name,reviews,geometry,formatted_address,wheelchair_accessible_entrance&key={GOOGLE_API_KEY}&language=es"
                details = requests.get(details_url).json().get('result', {})
                
                opiniones = [rev['text'] for rev in details.get('reviews', [])]
                
                lugar_data = {
                    "Place": details.get('name'),
                    "Location": nombre_alcaldia,
                    "x": str(details['geometry']['location']['lat']),
                    "y": str(details['geometry']['location']['lng']),
                    "bss_type": "Servicio Técnico/Médico", # <--- Categoría diferente
                    "sillas_ruedas": "Sí",
                    "estacionamiento": "Sí" if "estacionamiento" in str(opiniones).lower() else "No",
                    "rampas": "Sí",
                    "elevadores": "No",
                    "asistencia": "Sí",
                    "owner": "GOOGLE_SYSTEM",
                    "opiniones_brutas": opiniones,
                    "resumen_nlp": "Establecimiento especializado en equipo de movilidad y soporte técnico." 
                }
                
                db_name = details.get('name').replace('.', '').replace('#', '').replace('$', '').replace('[', '').replace(']', '')
                db.child("Lugares").child(db_name).set(lugar_data)
                print(f"   ✅ Re-agregado: {details.get('name')}")
                
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    agregar_servicios_tecnicos()