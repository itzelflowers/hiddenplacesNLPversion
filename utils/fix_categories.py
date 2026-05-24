import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.firebase import Firebase

db = Firebase().getdb()

# Palabras clave por categoría
PALABRAS_CLAVE = {
    "Comida": [
        "comida", "restaurante", "comer", "menú", "platillo", "cocina",
        "chef", "mesero", "desayuno", "almuerzo", "cena", "bebida",
        "taco", "sopa", "postre", "café", "buffet", "orden", "sabor",
        "rico", "delicioso", "precio", "propina"
    ],
    "Cultura": [
        "museo", "arte", "exposición", "historia", "cultural", "galería",
        "obra", "teatro", "concierto", "patrimonio", "arquitectura",
        "antiguo", "hacienda", "jardín", "parque", "visita", "recorrido"
    ],
    "Entretenimiento": [
        "diversión", "juego", "entretenimiento", "actividad", "experiencia",
        "familia", "niños", "atracción", "show", "espectáculo", "evento",
        "tour", "aventura", "deporte", "pista"
    ],
    "Salud": [
        "silla de ruedas", "silla ruedas", "ortopedia", "médico", "clínica",
        "hospital", "rehabilitación", "discapacidad", "prótesis", "terapia",
        "farmacia", "salud", "equipo médico", "oxígeno", "andadera",
        "muletas", "bastón", "accesibilidad", "reparación", "servicio médico"
    ]
}

def detectar_categoria(opiniones):
    if not opiniones:
        return None

    if isinstance(opiniones, list):
        texto = " ".join([op for op in opiniones if op]).lower()
    elif isinstance(opiniones, dict):
        texto = " ".join(opiniones.values()).lower()
    else:
        return None

    # Contar menciones por categoría
    conteos = {}
    for categoria, palabras in PALABRAS_CLAVE.items():
        conteos[categoria] = sum(1 for p in palabras if p in texto)

    # Retornar la categoría con más menciones
    mejor = max(conteos, key=conteos.get)
    
    # Solo cambiar si hay al menos 1 mención
    if conteos[mejor] > 0:
        return mejor
    return None

def corregir_categorias():
    lugares = db.child('Lugares').get()
    corregidos = 0
    sin_cambio = 0
    sin_opiniones = 0

    if lugares.each():
        for lugar in lugares.each():
            nombre = lugar.key()
            datos = lugar.val()

            if not datos:
                continue

            opiniones = datos.get('opiniones_brutas')
            categoria_actual = datos.get('bss_type', '')
            
            nueva_categoria = detectar_categoria(opiniones)

            if nueva_categoria and nueva_categoria != categoria_actual:
                db.child('Lugares').child(nombre).child('bss_type').set(nueva_categoria)
                print(f"✅ {nombre}: '{categoria_actual}' → '{nueva_categoria}'")
                corregidos += 1
            elif nueva_categoria is None:
                print(f"⚠️  {nombre}: sin opiniones suficientes")
                sin_opiniones += 1
            else:
                print(f"⬜ {nombre}: '{categoria_actual}' (sin cambio)")
                sin_cambio += 1

    print(f"\nResumen: {corregidos} corregidos, {sin_cambio} sin cambio, {sin_opiniones} sin opiniones.")

if __name__ == "__main__":
    corregir_categorias()