from ui.menu_monitoreo import iniciar_monitoreo
from ui.menu_web import menu_servicios_web
from ui.menu_internet import menu_test_internet

def menu_principal():
    while True:
        print("\n==============================================")
        print("   MINI SISTEMA DE MONITOREO DE RED - V.1.0")
        print("==============================================")
        print("1. Iniciar monitoreo de red y servicios académicos")
        print("2. Escanear servicios web")
        print("3. Test de calidad de internet")
        print("4. Salir del sistema")
        print("==============================================")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            iniciar_monitoreo()
        elif opcion == "2":
            menu_servicios_web()
        elif opcion == "3":
            menu_test_internet()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")
