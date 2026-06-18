import subprocess
import platform

def hacer_ping(dominio):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, "1", dominio]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return resultado.returncode == 0

def escanear_servicios_web():
    servicios = {
        "tupagina.cl": hacer_ping("tupagina.cl"),
        "tuotrapagina.cl": hacer_ping("tuotrapagina.cl"),
        "tu.pagina.cl": hacer_ping("tu.pagina.cl")
    }
    return servicios
