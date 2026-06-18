import subprocess
import re
import time
import platform
import smtplib
from email.message import EmailMessage
from datetime import datetime
import ssl

# ============================
# CONFIGURACIÓN DE DISPOSITIVOS
# ============================

AP = [
    {"nombre": "Repetidor tp-link-Inspectoria", "mac": "B0BE762DE159"},
    {"nombre": "Repetidor tp-link-PIE", "mac": "B0BE762DE131"},
    {"nombre": "Repetidor tp-link-Administracion", "mac": "B0BE762DE128"},
    {"nombre": "Servidor Web caprat.cl", "mac": ""},
    {"nombre": "Servidor Web napsis.com", "mac": ""}
]

# ============================
# CONFIGURACIÓN SMTP
# ============================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  
SMTP_USER = "reporte@caprat.cl"
SMTP_PASS = "ppjt cnrm vaqp uuqv"   
DESTINATARIO = "justhin.villagran@caprat.cl"

# ============================
# FUNCIÓN BASE DE ENVÍO (Estilo Script 1)
# ============================

def enviar_correo(asunto, cuerpo):
    mensaje = EmailMessage()
    mensaje["From"] = SMTP_USER
    mensaje["To"] = DESTINATARIO
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=contexto) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(mensaje)
        print(f"   => [SMTP ÉXITO] Correo enviado: '{asunto}'")
    except Exception as e:
        print(f"   => [SMTP ERROR] No se pudo enviar el correo.\n{e}")

# ============================
# FUNCIONES DE RED
# ============================

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

def escanear_red():
    """Escanea todos los APs y retorna un diccionario de estados junto con la lista de caídos."""
    estados = {}
    caidos = []
    
    for ap in AP:
        # Si tiene MAC, es un dispositivo local (AP)
        if ap["mac"]:
            ip = buscar_ip_por_mac(ap["mac"])
            esta_online = (ip and hacer_ping(ip))
            ip_mostrar = ip if ip else "No detectada"
        # Si NO tiene MAC, es un dominio externo (como caprat.cl)
        else:
            # Extraemos el dominio puro quitando texto extra si lo hubiera
            dominio = ap["nombre"].split()[-1] # Toma 'caprat.cl' del nombre
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

# ============================
# EJECUCIÓN DEL PROGRAMA
# ============================

if __name__ == "__main__":
    print("==============================================")
    print(" SISTEMA DE MONITOREO AUTOMÁTICO - CAPRAT     ")
    print("==============================================\n")

    # --------------------------------------------------------
    # 1. PASO INICIAL: Checklist de arranque (Acción Inmediata)
    # --------------------------------------------------------
    print("[1/2] Ejecutando Checklist Inicial de Arranque...")
    estados_iniciales, lista_caidos = escanear_red()
    
    fecha_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
    resumen_cuerpo = "Resultados del Checklist Inicial:\n\n"
    for nombre, datos in estados_iniciales.items():
        resumen_cuerpo += f"- {nombre}: {datos['estado']} (IP: {datos['ip']})\n"

    if len(lista_caidos) == 0:
        asunto_inicio = "[MONITOREO] Checklist Inicial: Dispositivos detectados"
        cuerpo_inicio = f"Dispositivos de red y página web operando correctamente.\n\n{resumen_cuerpo}\nHora de inicio: {fecha_hora}"
    else:
        asunto_inicio = f"[MONITOREO] Alerta Inicial: Dispositivos NO detectados ({len(lista_caidos)} CAÍDOS)"
        cuerpo_inicio = f"Atención. El sistema inició con anomalías en la red.\n\n{resumen_cuerpo}\nHora de inicio: {fecha_hora}"

    # Envío del correo obligatorio al iniciar
    enviar_correo(asunto_inicio, cuerpo_inicio)
    print(" Checklist enviado con éxito.\n")

    # Guardamos el estado inicial en la memoria del bucle
    estado_anterior = {nombre: datos["estado"] for nombre, datos in estados_iniciales.items()}

    # --------------------------------------------------------
    # 2. PASO CONTINUO: Bucle de monitoreo cada 60 segundos
    # --------------------------------------------------------
    print("[2/2] Pasando a modo de monitoreo activo continuo...")
    print("Escaneando red cada 60 segundos. Control + C para detener.\n")

    while True:
        time.sleep(60)  # Espera los 60 segundos antes del próximo chequeo
        print(f"--- Verificación de rutina: {datetime.now().strftime('%H:%M:%S')} ---")
        
        estados_actuales, _ = escanear_red()

        for nombre, datos in estados_actuales.items():
            estado_actual = datos["estado"]
            estado_prev = estado_anterior.get(nombre)

            # Imprimir traza en consola
            texto_consola = "OK" if estado_actual == "UP" else "SIN SERVICIO"
            print(f" > {nombre}: {texto_consola}")

            # Alertas en tiempo real ante CAMBIOS de estado
            if estado_prev and estado_prev != estado_actual:
                if estado_actual == "DOWN":
                    asunto_alerta = f"[ALERTA] {nombre} se ha CAÍDO"
                    cuerpo_alerta = f"El dispositivo {nombre} dejó de responder a los pings.\nIP de registro: {datos['ip']}\nHora del evento: {datetime.now().strftime('%H:%M:%S')}"
                else:
                    asunto_alerta = f"[RECOVERY] {nombre} restablecido"
                    cuerpo_alerta = f"El dispositivo {nombre} ha vuelto a estar en línea con éxito.\nIP de registro: {datos['ip']}\nHora del evento: {datetime.now().strftime('%H:%M:%S')}"
                
                enviar_correo(asunto_alerta, cuerpo_alerta)

            # Actualizar la memoria del bucle
            estado_anterior[nombre] = estado_actual
            
        print(" Monitoreo en orden. Esperando siguiente ciclo...\n")