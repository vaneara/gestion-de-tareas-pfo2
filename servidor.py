
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

DATABASE = "usuarios.db"


# Conexión y creación de la base de datos
def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tablas():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


# Endpoint para registrar usuarios
@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Debes enviar un JSON válido"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not isinstance(usuario, str) or not isinstance(contraseña, str):
        return jsonify({
            "error": "El usuario y la contraseña son obligatorios"
        }), 400

    usuario = usuario.strip()

    if not usuario or not contraseña:
        return jsonify({
            "error": "El usuario y la contraseña no pueden estar vacíos"
        }), 400

    if len(contraseña) < 4:
        return jsonify({
            "error": "La contraseña debe tener al menos 4 caracteres"
        }), 400

    contraseña_hash = generate_password_hash(contraseña)

    conexion = conectar_db()

    try:
        conexion.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )
        conexion.commit()

        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "El usuario ya existe"
        }), 409

    finally:
        conexion.close()


# Endpoint para iniciar sesión
@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Debes enviar un JSON válido"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not isinstance(usuario, str) or not isinstance(contraseña, str):
        return jsonify({
            "error": "El usuario y la contraseña son obligatorios"
        }), 400

    conexion = conectar_db()

    try:
        resultado = conexion.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario.strip(),)
        ).fetchone()
    finally:
        conexion.close()

    if resultado and check_password_hash(
        resultado["contraseña"], contraseña
    ):
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": resultado["usuario"]
        }), 200

    return jsonify({
        "error": "Usuario o contraseña incorrectos"
    }), 401


# Endpoint que muestra un HTML de bienvenida
@app.route("/tareas", methods=["GET"])
def tareas():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestión de Tareas</title>
    </head>
    <body>
        <h1>Bienvenido al Sistema de Gestión de Tareas</h1>
        <p>La API está funcionando correctamente.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    crear_tablas()
    app.run(debug=True)
