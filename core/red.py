import subprocess
import platform
import re

def normalizar_mac(mac):
    return re.sub(r'[^0-9a-fA-F]', '', mac).lower()

def obtener_tabla_arp():
    resultado = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    return resultado.stdout

def buscar_ip_por_mac(mac_objetivo):
    mac_objetivo = normalizar_mac(mac_objetivo)
    tabla = obtener_tabla_arp()

    for linea in tabla.splitlines():
        if "-" in linea or ":" in linea:
            partes = linea.split()
            if len(partes) >= 2:
                ip = partes[0]
                mac_en_tabla = normalizar_mac(partes[1])
                if mac_en_tabla == mac_objetivo:
                    return ip
    return None

def hacer_ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, "1", ip]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return resultado.returncode == 0
