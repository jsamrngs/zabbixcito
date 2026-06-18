from core.web_service import escanear_servicios_web

def menu_servicios_web():
    while True:
        print("\n=== ESCANEO DE SERVICIOS WEB ===")
        print("1. Ejecutar escaneo")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            servicios = escanear_servicios_web()
            print("\nResultados:")
            for dominio, estado in servicios.items():
                print(f" - {dominio}: {'OK' if estado else 'SIN RESPUESTA'}")
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
