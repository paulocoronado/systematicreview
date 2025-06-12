from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Paso 1: ir al proxy
    page.goto("https://login.bdigital.udistrital.edu.co/login?url=https://www.sciencedirect.com")

    print("Inicia sesión con Microsoft y espera la redirección a ScienceDirect")
    page.wait_for_timeout(90000)

    # Guardar sesión
    context.storage_state(path="sciencedirect_state.json")
    print("Sesión guardada en sciencedirect_state.json")
    browser.close()
