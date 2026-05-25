from utils.firebase import Firebase

db = Firebase().getdb()

LUGARES_SINTETICOS = {
    # =========================
    # COMIDA
    # =========================
    "Restaurante Accesible Tlalpan": {
        "Place": "Restaurante Accesible Tlalpan",
        "Location": "Tlalpan",
        "bss_type": "Comida",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.287500",
        "y": "-99.167000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "El restaurante tiene rampa en la entrada y estacionamiento amplio.",
            "Fuimos con una persona en silla de ruedas y el acceso fue cómodo.",
            "El personal fue amable y nos ayudó a encontrar una mesa accesible."
        ]
    },
    "Café Inclusivo Coyoacán": {
        "Place": "Café Inclusivo Coyoacán",
        "Location": "Coyoacán",
        "bss_type": "Comida",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.349000",
        "y": "-99.162000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene rampa y mesas cómodas para silla de ruedas.",
            "El personal fue amable con mi abuelita.",
            "No tiene estacionamiento propio, pero el acceso es sencillo."
        ]
    },
    "Comedor Familiar Benito Juárez": {
        "Place": "Comedor Familiar Benito Juárez",
        "Location": "Benito Juárez",
        "bss_type": "Comida",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "No",
        "resumen_nlp": "",
        "x": "19.380500",
        "y": "-99.160200",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "El lugar tiene rampa y estacionamiento cercano.",
            "Se puede entrar con silla de ruedas sin problema.",
            "La comida es buena y el espacio es amplio."
        ]
    },
    "Restaurante Familiar Miguel Hidalgo": {
        "Place": "Restaurante Familiar Miguel Hidalgo",
        "Location": "Miguel Hidalgo",
        "bss_type": "Comida",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.432000",
        "y": "-99.190000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene elevador y estacionamiento accesible.",
            "Es cómodo para adultos mayores.",
            "El personal ayuda a las personas con movilidad reducida."
        ]
    },
    "Taquería Accesible Iztapalapa": {
        "Place": "Taquería Accesible Iztapalapa",
        "Location": "Iztapalapa",
        "bss_type": "Comida",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.355000",
        "y": "-99.060000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene rampa en la entrada.",
            "El personal ayudó a acomodar la silla de ruedas.",
            "No tiene estacionamiento, pero el acceso es cómodo."
        ]
    },

    # =========================
    # ENTRETENIMIENTO
    # =========================
    "Parque Accesible La Villa": {
        "Place": "Parque Accesible La Villa",
        "Location": "Gustavo A. Madero",
        "bss_type": "Entretenimiento",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "No",
        "resumen_nlp": "",
        "x": "19.480000",
        "y": "-99.117000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Los caminos son amplios y se puede entrar con silla de ruedas.",
            "Tiene rampas en varias entradas.",
            "Hay estacionamiento cerca del acceso principal."
        ]
    },
    "Jardín Inclusivo Benito Juárez": {
        "Place": "Jardín Inclusivo Benito Juárez",
        "Location": "Benito Juárez",
        "bss_type": "Entretenimiento",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.380000",
        "y": "-99.160000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Es un lugar cómodo para caminar con una persona mayor.",
            "Tiene rampas y accesos sin escalones.",
            "El espacio es tranquilo y fácil de recorrer."
        ]
    },
    "Parque Familiar Coyoacán": {
        "Place": "Parque Familiar Coyoacán",
        "Location": "Coyoacán",
        "bss_type": "Entretenimiento",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "No",
        "resumen_nlp": "",
        "x": "19.347000",
        "y": "-99.160500",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Los caminos son accesibles.",
            "Hay estacionamiento cerca.",
            "Se puede recorrer con silla de ruedas."
        ]
    },
    "Bosque Accesible Tlalpan": {
        "Place": "Bosque Accesible Tlalpan",
        "Location": "Tlalpan",
        "bss_type": "Entretenimiento",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.300000",
        "y": "-99.190000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene zonas accesibles para silla de ruedas.",
            "Hay estacionamiento y apoyo del personal.",
            "Algunas áreas tienen rampas."
        ]
    },
    "Cine Accesible Universidad": {
        "Place": "Cine Accesible Universidad",
        "Location": "Coyoacán",
        "bss_type": "Entretenimiento",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.323000",
        "y": "-99.175000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene espacios para silla de ruedas.",
            "El elevador funciona bien.",
            "Hay estacionamiento accesible."
        ]
    },

    # =========================
    # CULTURA
    # =========================
    "Museo Accesible Coyoacán": {
        "Place": "Museo Accesible Coyoacán",
        "Location": "Coyoacán",
        "bss_type": "Cultura",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.350500",
        "y": "-99.162500",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "El museo tiene elevador y rampas.",
            "El personal ayuda a las personas con discapacidad.",
            "Es fácil recorrerlo en silla de ruedas."
        ]
    },
    "Centro Cultural Accesible Cuauhtémoc": {
        "Place": "Centro Cultural Accesible Cuauhtémoc",
        "Location": "Cuauhtémoc",
        "bss_type": "Cultura",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.432600",
        "y": "-99.133200",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene elevador y estacionamiento accesible.",
            "La entrada tiene rampa.",
            "El personal orienta muy bien a los visitantes."
        ]
    },
    "Galería Accesible Roma": {
        "Place": "Galería Accesible Roma",
        "Location": "Cuauhtémoc",
        "bss_type": "Cultura",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.418000",
        "y": "-99.160000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "La entrada tiene rampa.",
            "El personal ayuda durante el recorrido.",
            "El espacio es pequeño pero accesible."
        ]
    },
    "Museo con Estacionamiento Miguel Hidalgo": {
        "Place": "Museo con Estacionamiento Miguel Hidalgo",
        "Location": "Miguel Hidalgo",
        "bss_type": "Cultura",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "No",
        "resumen_nlp": "",
        "x": "19.425000",
        "y": "-99.190000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "El museo tiene elevador y rampas.",
            "Hay estacionamiento accesible.",
            "Se puede recorrer con silla de ruedas."
        ]
    },
    "Biblioteca Inclusiva Iztapalapa": {
        "Place": "Biblioteca Inclusiva Iztapalapa",
        "Location": "Iztapalapa",
        "bss_type": "Cultura",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.355500",
        "y": "-99.065000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene elevador y acceso amplio.",
            "La entrada cuenta con rampa.",
            "El personal ayuda a encontrar salas accesibles."
        ]
    },

    # =========================
    # SALUD / SERVICIO TÉCNICO
    # =========================
    "Ortopedia Accesible Tlalpan": {
        "Place": "Ortopedia Accesible Tlalpan",
        "Location": "Tlalpan",
        "bss_type": "Salud",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.288000",
        "y": "-99.166000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "La ortopedia tiene rampa y acceso cómodo.",
            "Atienden bien a personas en silla de ruedas.",
            "Tiene estacionamiento y personal de apoyo."
        ]
    },
    "Servicio Técnico de Sillas Coyoacán": {
        "Place": "Servicio Técnico de Sillas Coyoacán",
        "Location": "Coyoacán",
        "bss_type": "Servicio Técnico/Médico",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "No",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.346000",
        "y": "-99.161000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Reparan sillas de ruedas y tienen rampa en la entrada.",
            "El personal ayuda mucho.",
            "El local es pequeño pero accesible."
        ]
    },
    "Centro de Movilidad Benito Juárez": {
        "Place": "Centro de Movilidad Benito Juárez",
        "Location": "Benito Juárez",
        "bss_type": "Salud",
        "rampas": "Sí",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.380200",
        "y": "-99.158800",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "El lugar tiene rampas y elevador.",
            "Cuenta con estacionamiento accesible.",
            "El personal conoce bien el uso de sillas de ruedas."
        ]
    },
    "Reparación de Sillas Xochimilco": {
        "Place": "Reparación de Sillas Xochimilco",
        "Location": "Xochimilco",
        "bss_type": "Servicio Técnico/Médico",
        "rampas": "Sí",
        "elevadores": "No",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.255000",
        "y": "-99.105000",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Reparan sillas de ruedas y tienen estacionamiento.",
            "La entrada tiene rampa.",
            "La atención fue rápida y amable."
        ]
    },
    "Ortopedia Integral Cuauhtémoc": {
        "Place": "Ortopedia Integral Cuauhtémoc",
        "Location": "Cuauhtémoc",
        "bss_type": "Salud",
        "rampas": "No",
        "elevadores": "Sí",
        "sillas_ruedas": "Sí",
        "estacionamiento": "Sí",
        "asistencia": "Sí",
        "resumen_nlp": "",
        "x": "19.433500",
        "y": "-99.140500",
        "owner": "SYNTHETIC_DATA",
        "opiniones_brutas": [
            "Tiene elevador y personal atento.",
            "Hay estacionamiento.",
            "No vi rampa, pero sí hay apoyo para entrar."
        ]
    }
}


def insertar_lugares():
    insertados = 0
    omitidos = 0

    for nombre, datos in LUGARES_SINTETICOS.items():
        existente = db.child("Lugares").child(nombre).get().val()

        if existente:
            print(f"⚠️ Ya existe, se omite: {nombre}")
            omitidos += 1
            continue

        db.child("Lugares").child(nombre).set(datos)
        print(f"✅ Insertado: {nombre}")
        insertados += 1

    print("\nResumen")
    print(f"Insertados: {insertados}")
    print(f"Omitidos: {omitidos}")


if __name__ == "__main__":
    insertar_lugares()