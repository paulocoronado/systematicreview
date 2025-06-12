import re
from playwright.sync_api import sync_playwright
import random

def google_scholar_get_total_result(frase, en_titulo=True, tiempo_espera=10, headless=False):
    with sync_playwright() as p:
        # Lanzar el navegador en modo headless
        browser = p.chromium.launch(headless=headless, slow_mo=random.randint(100, 300))
        
        # Crear contexto para emular un navegador real
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-ES",  # Puedes cambiarlo a "en-US" si deseas resultados en inglés
            java_script_enabled=True
        )

        # Crear página
        page = context.new_page()

        # Desactivar la propiedad webdriver para evitar detección
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            # Abrir Google Scholar
            page.goto("https://scholar.google.com", timeout=tiempo_espera * 1000)

            # Verificar que no me está pidiendo CAPTCHA
            if "reCAPTCHA" in page.content():
                print("[ERROR] CAPTCHA detectado. No se puede continuar.")
                return -1

            query =  f"allintitle: {frase}" if en_titulo else frase
            page.fill('input[name="q"]', query)  # Introducir consulta
            page.keyboard.press("Enter")  # Simular tecla Enter
            page.wait_for_timeout(3000)  # Esperar 3 segundos por los resultados

            # Desplazamiento para simular interacción. Hacerlo lo más random posible
            page.mouse.wheel(0, 500)  # Desplazamiento hacia abajo
            page.wait_for_timeout(1000)  # Esperar un segundo tras cada scroll
            
            # Obtener contenido de la página
            texto_resultados = page.content()

            # Guardar el contenido en un archivo con nombre único
            with open(f"resultado_{frase.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
                f.write(texto_resultados)

            # Buscar el número de resultados (tanto en español como en inglés)
            match = re.search(r"([\d.,]+)\s+(resultados?|results?)", texto_resultados, re.IGNORECASE)
            
            if not match:
                # Fallback: buscar solo número
                match = re.search(r"([\d.,]+)", texto_resultados)

            # Si encontramos el número, lo devolvemos
            if match:
                numero = match.group(1).replace(",", "").replace(".", "")
                return int(numero)
            return 0
        except Exception as e:
            print(f"[ERROR] Frase: '{frase}' → {e}")
            return -1
        finally:
            browser.close()  # Cerrar el navegador

