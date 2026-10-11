import requests

URL = "http://127.0.0.1:5000"


def menu():
    while True:
        print("\n--- SISTEMA DE GESTIÓN DE TAREAS ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = input("Usuario: ")
            contraseña = input("Contraseña: ")

            respuesta = requests.post(
                f"{URL}/registro",
                json={"usuario": usuario, "contraseña": contraseña}
            )
            print(respuesta.status_code, respuesta.json())

        elif opcion == "2":
            usuario = input("Usuario: ")
            contraseña = input("Contraseña: ")

            respuesta = requests.post(
                f"{URL}/login",
                json={"usuario": usuario, "contraseña": contraseña}
            )
            print(respuesta.status_code, respuesta.json())

        elif opcion == "3":
            print("Hasta luego.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()