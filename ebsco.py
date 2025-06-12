# ebsco_buscar.py

from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="ebsco_state.json")  # Usa la sesión guardada
    page = context.new_page()

    # Ir directamente a la página de búsqueda
    page.goto("https://research-ebsco-com.bdigital.udistrital.edu.co/c/4hxct6/search")
    page.wait_for_load_state("networkidle")

    # Esperar que el campo con id="search-input" esté visible
    page.wait_for_selector("#search-input", timeout=10000)

    # Escribir término de búsqueda y enviar
    search_box = page.locator("#search-input")
    search_box.fill("inteligencia artificial en educación")
    search_box.press("Enter")
    print("✅ Búsqueda enviada")

    sleep(10)  # Esperar resultados
    browser.close()
