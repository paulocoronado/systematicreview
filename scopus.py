from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="scopus_state.json")
    page = context.new_page()

    # Ir directamente a Scopus ya autenticado
    page.goto("https://www.scopus.com/home.url")
    page.wait_for_load_state("networkidle")

    # Localizar y llenar campo de búsqueda
    page.wait_for_selector("input[name='searchterm1']", timeout=10000)
    search_box = page.locator("input[name='searchterm1']")
    search_box.fill("inteligencia artificial en educación")
    search_box.press("Enter")

    print("✅ Búsqueda enviada")
    sleep(10)
    browser.close()
