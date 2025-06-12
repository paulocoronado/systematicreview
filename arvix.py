import requests
import xml.etree.ElementTree as ET

def arxiv_get_total_result(frase, max_results=1):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{frase}",
        "start": 0,
        "max_results": max_results
    }

    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        
        # Extraer el total desde <opensearch:totalResults>
        total_results = root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text
        print(f"Frase: {frase} → Resultados: {total_results}")
        return int(total_results)
    except Exception as e:
        print(f"❌ Error con arXiv y frase '{frase}': {e}")
        return -1
arxiv_get_total_result("inteligencia artificial en educación")