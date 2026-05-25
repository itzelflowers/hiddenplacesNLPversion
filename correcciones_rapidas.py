from utils.firebase import Firebase

db = Firebase().getdb()

CORRECCIONES = {
    # Salud / ortopedia
    "Fluchaire Ortopedicos": "Salud",

    # Parques / espacios naturales
    "Bosque de Tláhuac": "Entretenimiento",
    "Los Dinamos": "Entretenimiento",
    "PARQUE ACTEAL": "Entretenimiento",
    "Parque Ecológico de Xochimilco": "Entretenimiento",
    "Parque Ecoturístico Toltenco Mágico": "Entretenimiento",
    "Parque El Batán": "Entretenimiento",
    "Parque Escuela Urbano Ecológico Iztacalco": "Entretenimiento",
    "Parque La Mexicana": "Entretenimiento",
    "Parque Natural La Cañada": "Entretenimiento",
    "Parque Tezozómoc": "Entretenimiento",
    "Jardín Centenario": "Entretenimiento",
    "Jardín De Tlalpan": "Entretenimiento",
}


def aplicar_correcciones():
    lugares = db.child("Lugares").get().val()

    if not lugares:
        print("No se encontraron lugares.")
        return

    corregidos = 0
    no_encontrados = 0

    for nombre_objetivo, nueva_categoria in CORRECCIONES.items():
        encontrado = False

        for firebase_id, datos in lugares.items():
            if not isinstance(datos, dict):
                continue

            nombre_place = datos.get("Place", "")
            
            # Comparamos tanto contra la llave de Firebase como contra el campo Place
            if firebase_id == nombre_objetivo or nombre_place == nombre_objetivo:
                encontrado = True
                categoria_actual = datos.get("bss_type", "N/A")

                db.child("Lugares").child(firebase_id).update({
                    "bss_type": nueva_categoria
                })

                # Verificación inmediata
                datos_actualizados = db.child("Lugares").child(firebase_id).get().val()
                categoria_guardada = datos_actualizados.get("bss_type", "N/A")

                print(
                    f"✅ {nombre_objetivo}: "
                    f"{categoria_actual} → {categoria_guardada}"
                )

                corregidos += 1
                break

        if not encontrado:
            print(f"⚠️ No encontrado: {nombre_objetivo}")
            no_encontrados += 1

    print("\nResumen")
    print(f"Corregidos: {corregidos}")
    print(f"No encontrados: {no_encontrados}")


if __name__ == "__main__":
    aplicar_correcciones()