import requests
import time
import random

def random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
    ]
    return random.choice(agents)

def search_semantic_scholar(query, limit=1, retries=5, max_backoff=60):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title"
    }

    backoff = 10  # segundos
    for attempt in range(retries):
        headers = {"User-Agent": random_user_agent()}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            # Reiniciar backoff tras éxito
            return total

        elif response.status_code == 429:
            print(f"[WARN] Límite alcanzado. Reintentando en {backoff} segundos...")
            time.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)

        else:
            print(f"[ERROR] Consulta fallida para: {query} → Código: {response.status_code}")
            return -1

    print(f"[ERROR] Se alcanzó el número máximo de reintentos para: {query}")
    print("Esperando 5 minutos antes de continuar...")
    time.sleep(300)
    return -1
