import sys
import time
import random

def sleep_with_progress(min_sec=30, max_sec=60):
    total = random.randint(min_sec, max_sec)
    print(f"\nEsperando {total} segundos para evitar bloqueo de Google Scholar...\n")
    for i in range(total):
        time.sleep(1)
        progress = int((i + 1) / total * 50)  # 50 caracteres de ancho
        sys.stdout.write(f"\r[{'█' * progress}{'.' * (50 - progress)}] {i + 1}/{total}s")
        sys.stdout.flush()
    print()  # salto de línea después de la barra