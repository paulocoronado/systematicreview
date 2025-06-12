import pandas as pd

def extraer_palabras(texto):
    if pd.isna(texto):
        return set()
    return set(texto.replace('"', '').replace('+', ' ').strip().split())

def generar_combinaciones(ruta_archivo, hoja=0, salida="frases_combinadas.xlsx"):
    df = pd.read_excel(ruta_archivo, sheet_name=hoja)
    df.columns = ['Columna1', 'Columna2']

    resultados = []

    for i, fila1 in df.iterrows():
        palabras1 = extraer_palabras(fila1['Columna1'])
        for j, fila2 in df.iterrows():
            palabras2 = extraer_palabras(fila2['Columna2'])

            # Verificar si hay al menos una palabra en común
            if palabras1 & palabras2:
                combinadas = palabras1.union(palabras2)
                frase = ' + '.join(sorted(combinadas))
                resultados.append({
                    'Columna1': fila1['Columna1'],
                    'Columna2': fila2['Columna2'],
                    'FraseCombinada': frase
                })

    # Guardar resultados en un nuevo archivo
    resultado_df = pd.DataFrame(resultados)
    resultado_df.to_excel(salida, index=False)
    print(f"✅ Archivo generado: {salida}")

if __name__ == "__main__":
    generar_combinaciones("frases_busqueda.xlsx")
