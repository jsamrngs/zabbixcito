import time
from datetime import datetime
from core.monitor import escanear_red
from core.mail import enviar_correo

def iniciar_monitoreo():
    print("\n=== MODO MONITOREO CONTINUO ===")
    print("Presiona CTRL + C para detener.\n")

    estados_previos, caidos = escanear_red()
    estado_anterior = {n: d["estado"] for n, d in estados_previos.items()}

    resumen = "\n".join(
        f"- {n}: {d['estado']} (IP: {d['ip']})"
        for n, d in estados_previos.items()
    )
    enviar_correo("[MONITOREO] Inicio del sistema", resumen)

    ultimo_reporte = None
    HORA_REPORTE = "08:00"

    while True:
        try:
            time.sleep(60)
            estados_actuales, _ = escanear_red()

            print("\n--- Estado anterior ---")
            for nombre, estado in estado_anterior.items():
                print(f" > {nombre}: {'OK' if estado == 'UP' else 'SIN SERVICIO'}")

            print("\n--- Estado actual ---")
            for nombre, datos in estados_actuales.items():
                estado_actual = datos["estado"]
                print(f" > {nombre}: {'OK' if estado_actual == 'UP' else 'SIN SERVICIO'}")

            for nombre, datos in estados_actuales.items():
                estado_actual = datos["estado"]
                estado_prev = estado_anterior.get(nombre)

                if estado_prev != estado_actual:
                    if estado_actual == "DOWN":
                        enviar_correo(
                            f"[ALERTA] {nombre} CAÍDO",
                            f"{nombre} dejó de responder.\nIP: {datos['ip']}"
                        )
                    else:
                        enviar_correo(
                            f"[RECOVERY] {nombre} OK",
                            f"{nombre} volvió a responder.\nIP: {datos['ip']}"
                        )

                estado_anterior[nombre] = estado_actual

            hora_actual = datetime.now().strftime("%H:%M")
            if hora_actual == HORA_REPORTE and ultimo_reporte != datetime.now().date():
                resumen_diario = "\n".join(
                    f"- {n}: {('OK' if e=='UP' else 'SIN SERVICIO')}"
                    for n, e in estado_anterior.items()
                )
                enviar_correo("[REPORTE DIARIO]", resumen_diario)
                ultimo_reporte = datetime.now().date()

            print("\nMonitoreo en orden. Esperando siguiente ciclo...\n")

        except KeyboardInterrupt:
            print("\nMonitoreo detenido por el usuario.\n")
            break
