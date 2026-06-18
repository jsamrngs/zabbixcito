from core.red import buscar_ip_por_mac, hacer_ping
from core.mail import enviar_correo
from config.device import AP
from datetime import datetime

def escanear_red():
    estados = {}
    caidos = []

    for ap in AP:
        if ap["mac"]:
            ip = buscar_ip_por_mac(ap["mac"])
            esta_online = (ip and hacer_ping(ip))
            ip_mostrar = ip if ip else "No detectada"
        else:
            dominio = ap["nombre"].split()[-1]
            esta_online = hacer_ping(dominio)
            ip_mostrar = "Dominio Público"

        estado_actual = "UP" if esta_online else "DOWN"

        estados[ap["nombre"]] = {
            "estado": estado_actual,
            "ip": ip_mostrar
        }

        if not esta_online:
            caidos.append(ap["nombre"])

    return estados, caidos
