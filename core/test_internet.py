import subprocess
import platform
import re

def test_internet():
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, "4", "8.8.8.8"]

    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    salida = resultado.stdout

    # ============================
    # 1. Windows en español
    # ============================
    match = re.search(r"recibidos = (\d+)", salida, re.IGNORECASE)

    # ============================
    # 2. Windows en inglés (fallback)
    # ============================
    if not match:
        match = re.search(r"Received = (\d+)", salida, re.IGNORECASE)

    # ============================
    # 3. Linux / MacOS
    # ============================
    if not match:
        match = re.search(r"(\d+) received", salida, re.IGNORECASE)

    # ============================
    # Si aún no encuentra nada
    # ============================
    if not match:
        return {"estado": "ERROR", "recibidos": 0}

    recibidos = int(match.group(1))

    # Diagnóstico
    if recibidos == 4:
        estado = "EXCELENTE"
    elif recibidos == 3:
        estado = "INTERMITENCIA LEVE"
    elif recibidos == 2:
        estado = "INTERMITENCIA MODERADA"
    elif recibidos == 1:
        estado = "INTERMITENCIA GRAVE"
    else:
        estado = "SIN INTERNET"

    return {
        "estado": estado,
        "recibidos": recibidos
    }
