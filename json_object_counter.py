import os
import json
import pandas as pd
from pathlib import Path

def procesar_json_en_directorio(directorio, salida_excel="resumen_archivos_json.xlsx"):
    datos = []

    # Recorre todos los archivos .json del directorio
    for nombre_archivo in os.listdir(directorio):
        if nombre_archivo.endswith(".json") and nombre_archivo.startswith("filtrado_"):
            ruta_completa = os.path.join(directorio, nombre_archivo)
            try:
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    nombre_limpio = Path(nombre_archivo).stem.replace("filtrado_", "")
                    cantidad = len(json_data)
                    datos.append((nombre_limpio, cantidad))
            except Exception as e:
                print(f"Error procesando {nombre_archivo}: {e}")

    # Crear el DataFrame
    df = pd.DataFrame(datos, columns=["NombreArchivo", "CantidadObjetos"])

    # Guardar como archivo Excel
    ruta_salida = os.path.join(directorio, salida_excel)
    df.to_excel(ruta_salida, index=False)
    print(f"Resumen guardado en: {ruta_salida}")

# Ejemplo de uso
if __name__ == "__main__":
    directorio = "resultados_openalex"  # Cambia esto por la ruta de tu directorio
    procesar_json_en_directorio(directorio)