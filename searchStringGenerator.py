import pandas as pd
import itertools

def generar_frases_combinadas(ruta_archivo, hoja=0):
    df = pd.read_excel(ruta_archivo, sheet_name=hoja)
    if 'Nivel1' not in df.columns or 'Nivel2' not in df.columns:
        raise ValueError("El archivo debe contener las columnas 'Nivel1' y 'Nivel2'")
    
    nivel1 = df['Nivel1'].dropna().drop_duplicates().tolist()
    nivel2 = df['Nivel2'].dropna().drop_duplicates().tolist()
    
    frases = [f'"{n1}"+"{n2}"' for n1, n2 in itertools.product(nivel1, nivel2)]
    return frases

def generar_frases_columnas(ruta_archivo, hoja=0):
    df = pd.read_excel(ruta_archivo, sheet_name=hoja)

    
    if 'Frases' not in df.columns:
        raise ValueError("El archivo debe contener la columna 'Frases'")

    col_frases= df['Frases'].dropna().drop_duplicates().tolist()   
        
    frases = [f'{n1}' for n1 in col_frases]
    return frases

import pandas as pd
import itertools

def generar_frases_combinadas_total(ruta_archivo, hoja=0):
    df = pd.read_excel(ruta_archivo, sheet_name=hoja)

    # Validar columnas
    for col in ['Nivel1', 'Nivel2', 'Nivel3']:
        if col not in df.columns:
            raise ValueError(f"El archivo debe contener la columna '{col}'")

    # Obtener listas sin nulos ni duplicados
    nivel1 = df['Nivel1'].dropna().drop_duplicates().tolist()
    nivel2 = df['Nivel2'].dropna().drop_duplicates().tolist()
    nivel3 = df['Nivel3'].dropna().drop_duplicates().tolist()

    # Crear combinaciones
    frases = [f'"{n1}"+"{n2}"+"{n3}"' for n1, n2, n3 in itertools.product(nivel1, nivel2, nivel3)]

    return frases