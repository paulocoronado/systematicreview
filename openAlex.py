import requests
import json
import os
import re
from time import sleep

def openalex_get_total_result(frase, tipo="display_name", mailto="osgeolab@udistrital.edu.co"):
    base_url = "https://api.openalex.org/works"
    
    # Options: title_and_abstract, display_name
    params = {
        "filter": f"{tipo}.search:{frase}",
        "mailto": mailto,
        "per-page": 1  # Solo nos interesa el total
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        total = data.get("meta", {}).get("count", 0)
        print(f"Frase: {frase} → Resultados: {total}")
        return total
    except Exception as e:
        print(f"Error al consultar '{frase}': {e}")
        return -1



def reconstruir_abstract(abstract_index):
    if not abstract_index:
        return "No disponible"
    palabras = sorted(abstract_index.items(), key=lambda item: min(item[1]))
    return " ".join([palabra for palabra, _ in palabras])

def openalex_extraer_datos(frase, mailto="osgeolab@udistrital.edu.co", output_folder="resultados_openalex", per_page=200):
    base_url = "https://api.openalex.org/works"
    frase_sanitizada = re.sub(r'[^\w\s-]', '', frase).strip().replace(" ", "_")
    os.makedirs(output_folder, exist_ok=True)

    resultados_filtrados = []
    page = 1
    total_count = None

    while True:
        params = {
            "filter": f"display_name.search:{frase}",
            "sort": "relevance_score:desc",
            "per-page": per_page,
            "page": page,
            "mailto": mailto
        }

        try:
            response = requests.get(base_url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            if total_count is None:
                total_count = data.get("meta", {}).get("count", 0)
                print(f"🔢 Total de resultados: {total_count}")

            resultados = data.get("results", [])
            if not resultados:
                break

            for work in resultados:
                if work.get("language") != "en":
                    continue  # solo inglés

                abstract_text = reconstruir_abstract(work.get("abstract_inverted_index"))
                resultado = {
                    "id": work.get("id"),
                    "doi": work.get("doi"),
                    "title": work.get("title"),
                    "display_name": work.get("display_name"),
                    "relevance_score": work.get("relevance_score"),
                    "publication_year": work.get("publication_year"),
                    "language": work.get("language"),
                    "abstract": abstract_text
                }
                resultados_filtrados.append(resultado)

            print(f"📄 Página {page} procesada. Resultados en inglés acumulados: {len(resultados_filtrados)}")

            if len(resultados_filtrados) >= total_count:
                break

            page += 1
            sleep(1)  # evitar rate limits

        except Exception as e:
            print(f"❌ Error en la página {page}: {e}")
            break

    # Guardar resultados como JSON
    filename = os.path.join(output_folder, f"filtrado_{frase_sanitizada}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(resultados_filtrados, f, ensure_ascii=False, indent=2)

    print(f"✅ Resultados filtrados guardados en: {filename}")



