import requests
from bs4 import BeautifulSoup
import re

def eric_search_result(frase, en_titulo=True):
    base_url = "https://eric.ed.gov/"
    if en_titulo:
        query = f'title:"{frase}"'
    else:
        query = frase

    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0"  # Para evitar bloqueos por bots
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar el texto como "1–10 of 3,454 results"
        resultado = soup.find("div", class_="results-count")
        if resultado:
            texto = resultado.text
            print(f"Frase: {frase} → Texto: {texto}")
            match = re.search(r"of\s+([\d,]+)", texto)
            if match:
                numero = match.group(1).replace(",", "")
                return int(numero)
        return 0

    except Exception as e:
        print(f"Error con frase '{frase}': {e}")
        return -1


