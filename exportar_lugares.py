import pandas as pd
from utils.firebase import Firebase

db = Firebase().getdb()

lugares_data = db.child("Lugares").get().val()

if not lugares_data:
    print("No se encontraron lugares en Firebase.")
    exit()

filas = []

for lugar_id, datos in lugares_data.items():
    if isinstance(datos, dict):
        fila = datos.copy()
        fila["firebase_id"] = lugar_id
        filas.append(fila)

df = pd.DataFrame(filas)

columnas_ordenadas = [
    "firebase_id",
    "Place",
    "Location",
    "bss_type",
    "rampas",
    "elevadores",
    "sillas_ruedas",
    "estacionamiento",
    "asistencia",
    "resumen_nlp",
    "x",
    "y",
    "owner"
]

columnas_existentes = [c for c in columnas_ordenadas if c in df.columns]
otras_columnas = [c for c in df.columns if c not in columnas_existentes]

df = df[columnas_existentes + otras_columnas]

df.to_csv("lugares_exportados.csv", index=False, encoding="utf-8-sig")

print(f"Archivo generado: lugares_exportados.csv")
print(f"Número de lugares exportados: {len(df)}")
print("Columnas:")
print(df.columns.tolist())