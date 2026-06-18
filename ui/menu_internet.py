from core.test_internet import test_internet
from core.mail import enviar_correo

def menu_test_internet():
    while True:
        print("\n=== TEST DE CALIDAD DE INTERNET ===")
        print("1. Ejecutar test")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            print("\nRealizando test...\n")
            resultado = test_internet()

            estado = resultado["estado"]
            recibidos = resultado["recibidos"]

            print(f"Paquetes recibidos: {recibidos}/4")
            print(f"Diagnóstico: {estado}")

            if estado != "EXCELENTE":
                enviar_correo(
                    "[ALERTA] Intermitencia con el proveedor Movistar",
                    f"Se detectó un problema en la calidad del internet.\n"
                    f"Paquetes recibidos: {recibidos}/4\n"
                    f"Diagnóstico: {estado}"
                )
                print("Correo de alerta enviado.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
