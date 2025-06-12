from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()  # NO cargamos storage_state aquí
    page = context.new_page()

    # Ir al enlace de login
    page.goto("https://login.bdigital.udistrital.edu.co/login?url=https://search.ebscohost.com/login.aspx?authtype=ip,uid&custid=ns000601&groupid=main&profile=ehost")

    print("🔐 Haz login con Microsoft. Tienes 90 segundos...")
    page.wait_for_timeout(90000)

    # ✅ Guardar la sesión (cookies + localStorage)
    context.storage_state(path="ebsco_state.json")
    print("✅ Sesión guardada en 'ebsco_state.json'")
    browser.close()
