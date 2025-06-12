from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Ir a Scopus por el proxy institucional
    page.goto("https://login.bdigital.udistrital.edu.co/login?url=https://www.scopus.com/home.url")

    print("🔐 Inicia sesión con Microsoft. Se guardará la sesión en 90 segundos.")
    page.wait_for_timeout(90000)

    context.storage_state(path="scopus_state.json")
    print("✅ Sesión guardada en scopus_state.json")
    browser.close()
