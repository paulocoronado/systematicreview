from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="sciencedirect_state.json")
    page = context.new_page()

    # Ir directamente a ScienceDirect con sesión guardada
    page.goto("https://www.sciencedirect.com/")
    page.wait_for_load_state("networkidle")

    # Buscar
    page.wait_for_selector("input[id='qs-searchbox-input']", timeout=10000)
    search_box = page.locator("input[id='qs-searchbox-input']")
    search_box.fill("inteligencia artificial en educación")
    search_box.press("Enter")

    print("✅ Búsqueda enviada")
    sleep(10)
    browser.close()
