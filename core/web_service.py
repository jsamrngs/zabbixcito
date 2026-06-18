import subprocess
import platform

def hacer_ping(dominio):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, "1", dominio]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return resultado.returncode == 0

def escanear_servicios_web():
    servicios = {
        "caprat.cl": hacer_ping("caprat.cl"),
        "napsis.cl": hacer_ping("napsis.cl"),
        "sige.mineduc.cl": hacer_ping("sige.mineduc.cl")
    }
    return servicios
