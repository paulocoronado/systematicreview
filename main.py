import pandas as pd
import time
import random
from searchStringGenerator import generar_frases_combinadas
from searchStringGenerator import generar_frases_columnas
from googleScholar import google_scholar_get_total_result
from sleep_with_progress import sleep_with_progress
from semanticScholar import search_semantic_scholar
from openAlex import openalex_extraer_datos
from openAlex import openalex_get_total_result

def buscar_frases_google_scholar():
    #frases = generar_frases_combinadas("TérminosDeBúsqueda.xlsx")

    frases = generar_frases_columnas("frases.xlsx")

    print(f"Frases generadas: {len(frases)}")
    random.shuffle(frases)

    resultados = []
    for frase in frases:
        total = google_scholar_get_total_result(frase)
        print(f"{frase} → {total}")
        resultados.append((frase, total))
        sleep_with_progress(60, 90)

    df = pd.DataFrame(resultados, columns=["Frase", "Cantidad de Resultados"])
    df.to_excel("resultados_google_scholar_playwright.xlsx", index=False)
    print("Archivo guardado: resultados_google_scholar_playwright.xlsx")

def buscar_frases_semantic_scholar():
    frases = generar_frases_combinadas("TérminosDeBúsqueda.xlsx")
    print(f"Frases generadas: {len(frases)}")

    random.shuffle(frases)  # Desordenar las frases para evitar patrones repetitivos

    resultados = []
    for frase in frases:
        print(f"🔍 Consultando: {frase}")
        total = search_semantic_scholar(frase)
        print(f"{frase} → {total}")
        resultados.append((frase, total))

        wait = random.randint(7, 20)  # Espera más realista
        print(f"Esperando {wait} segundos...\n")
        time.sleep(wait)

    df = pd.DataFrame(resultados, columns=["Frase", "Cantidad de Resultados"])
    df.to_excel("resultados_semantic_scholar.xlsx", index=False)
    print("Archivo generado: resultados_semantic_scholar.xlsx")

def search_openalex():
    frases = generar_frases_columnas("frases_combinadas.xlsx")
    print(f"Frases generadas: {len(frases)}")
    random.shuffle(frases)
    resultados = []
    for frase in frases:
        print(f"🔍 Consultando: {frase}")
        total = openalex_get_total_result(frase)
        print(f"{frase} → {total}")
        resultados.append((frase, total))

        wait = random.randint(7, 10)  # Espera más realista
        print(f"Esperando {wait} segundos...\n")
        time.sleep(wait)

    df = pd.DataFrame(resultados, columns=["Frase", "Cantidad de Resultados"])
    df.to_excel("resultados_open_alex.xlsx", index=False)
    print("Archivo generado")

def json_openalex():
    frases = generar_frases_columnas("frases_combinadas.xlsx")
    print(f"Frases generadas: {len(frases)}")
    random.shuffle(frases)
    for frase in frases:
        print(f"🔍 Consultando: {frase}")
        openalex_extraer_datos(frase)
        wait = random.randint(7, 10)  # Espera más realista
        print(f"Esperando {wait} segundos...\n")
        time.sleep(wait)    


if __name__ == "__main__":
    json_openalex()
