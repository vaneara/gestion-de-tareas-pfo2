# PFO 2 — Sistema de Gestión de Tareas
Aracena Vanesa - 3°E

## Descripción del proyecto
Implementación de API REST utilizando Python y Flask, con persistencia de datos mediante SQLite. Permite registrar usuarios, verificar sus credenciales e ingresar a una página HTML de bienvenida.
Las contraseñas se almacenan mediante hashing para evitar guardar las claves originales en texto plano.

## Tecnologías utilizadas
- Python
- Flask
- SQLite
- Werkzeug para el hashing de contraseñas
- Requests para probar la API desde la consola


## Instrucciones para ejecutar y probar
**1. Crear el entorno virtual e instalar las dependencias**
```bash
python -m venv .venv
```

En Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install Flask Werkzeug requests
```

**2. Iniciar el servidor**
```bash
python servidor.py
```
Dejar la terminal abierta mientras se realizan las pruebas.

**3. Ejecutar el cliente en consola**
Abrir una segunda terminal en la carpeta del proyecto, activar el entorno virtual y ejecutar:

```bash
python cliente.py
```

**4. Probar las opciones del menú**
- **Opción 1:** registrar un usuario nuevo.
- **Opción 2:** iniciar sesión con las credenciales registradas.
- Probar también con una contraseña incorrecta para verificar el rechazo del acceso.
- **Opción 3:** salir del cliente.

El cliente muestra los códigos HTTP y las respuestas que devuelve la API.

La página HTML de bienvenida también puede consultarse desde el navegador en http://127.0.0.1:5000/tareas.


## Respuestas conceptuales

### 1. ¿Por qué hashear contraseñas?
El hashing permite almacenar una representación de la contraseña en lugar de guardar su valor original en texto plano. Así, si alguien accede a la base de datos, no podrá leer directamente las contraseñas almacenadas.
Durante el inicio de sesión, la aplicación utiliza una función de verificación para comprobar si la contraseña ingresada coincide con el hash guardado. Esto mejora la seguridad de las cuentas de los usuarios.

### 2. ¿Cuáles son las ventajas de usar SQLite en este proyecto?
SQLite es una base de datos liviana que no necesita instalar ni administrar un servidor de base de datos independiente. Guarda la información en un archivo local y permite realizar operaciones SQL de forma sencilla.
Es adecuada para este proyecto académico porque facilita la persistencia de los usuarios, simplifica la instalación y permite trabajar con Python mediante el módulo `sqlite3`, incluido en su biblioteca estándar.

