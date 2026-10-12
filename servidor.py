
from flask import (
    Flask, request, jsonify, redirect, url_for,
    session, flash, render_template_string
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "testkey"

DATABASE = "usuarios.db"


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


# Diseño de la web
PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ titulo }} - Gestión de Tareas</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f3f0;
            color: #333;
        }
        header {
            background: #315b50;
            color: white;
            padding: 22px;
            text-align: center;
        }
        main {
            max-width: 430px;
            margin: 45px auto;
            padding: 28px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 18px #00000012;
        }
        h2 { text-align: center; }
        label { display: block; margin-top: 16px; }
        input {
            width: 100%;
            padding: 12px;
            margin-top: 7px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        button, .boton {
            display: block;
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            border: none;
            border-radius: 6px;
            background: #315b50;
            color: white;
            text-align: center;
            text-decoration: none;
            cursor: pointer;
            font-size: 16px;
        }
        .mensaje {
            background: #e5f4e8;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 12px;
        }
        .error { background: #fbe5e5; }
        .enlaces { text-align: center; margin-top: 20px; }
        .enlaces a { color: #315b50; }
    </style>
</head>
<body>
    <header>
        <h1>Gestión de Tareas</h1>
        <p>PFO 2 · API Flask y SQLite</p>
    </header>
    <main>
        <h2>{{ titulo }}</h2>

        {% for categoria, mensaje in get_flashed_messages(with_categories=true) %}
            <div class="mensaje {{ categoria }}">{{ mensaje }}</div>
        {% endfor %}

        {{ contenido|safe }}
    </main>
</body>
</html>
"""


def pagina(titulo, contenido):
    return render_template_string(
        PLANTILLA, titulo=titulo, contenido=contenido
    )


@app.route("/")
def inicio():
    contenido = """
    <p>Bienvenido al sistema de gestión de tareas.</p>
    <a class="boton" href="/registro-web">Crear una cuenta</a>
    <a class="boton" href="/login-web">Iniciar sesión</a>
    """
    return pagina("Inicio", contenido)


# API: registro mediante JSON
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

    conexion = conectar_db()
    try:
        conexion.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, generate_password_hash(contraseña))
        )
        conexion.commit()
        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    finally:
        conexion.close()


# API: login 
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


# Formulario de registro
@app.route("/registro-web", methods=["GET", "POST"])
def registro_web():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contraseña = request.form.get("contraseña", "")

        if not usuario or not contraseña:
            flash("Completá todos los campos.", "error")
        elif len(contraseña) < 4:
            flash("La contraseña debe tener al menos 4 caracteres.", "error")
        else:
            conexion = conectar_db()
            try:
                conexion.execute(
                    "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
                    (usuario, generate_password_hash(contraseña))
                )
                conexion.commit()
                flash("Usuario registrado correctamente. Ya podés ingresar.", "")
                return redirect(url_for("login_web"))
            except sqlite3.IntegrityError:
                flash("Ese usuario ya existe. Elegí otro.", "error")
            finally:
                conexion.close()

    contenido = """
    <form method="POST">
        <label for="usuario">Nombre de usuario</label>
        <input id="usuario" name="usuario" required maxlength="80">

        <label for="contraseña">Contraseña (mínimo 4 caracteres)</label>
        <input id="contraseña" name="contraseña" type="password"
               minlength="4" required>

        <button type="submit">Registrarme</button>
    </form>
    <div class="enlaces"><a href="/login-web">Ya tengo una cuenta</a></div>
    """
    return pagina("Crear cuenta", contenido)


# Formulario de inicio de sesión
@app.route("/login-web", methods=["GET", "POST"])
def login_web():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contraseña = request.form.get("contraseña", "")

        conexion = conectar_db()
        try:
            resultado = conexion.execute(
                "SELECT * FROM usuarios WHERE usuario = ?",
                (usuario,)
            ).fetchone()
        finally:
            conexion.close()

        if resultado and check_password_hash(
            resultado["contraseña"], contraseña
        ):
            session["usuario"] = resultado["usuario"]
            return redirect(url_for("tareas"))

        flash("Usuario o contraseña incorrectos.", "error")

    contenido = """
    <form method="POST">
        <label for="usuario">Nombre de usuario</label>
        <input id="usuario" name="usuario" required>

        <label for="contraseña">Contraseña</label>
        <input id="contraseña" name="contraseña"
               type="password" required>

        <button type="submit">Iniciar sesión</button>
    </form>
    <div class="enlaces"><a href="/registro-web">Crear una cuenta</a></div>
    """
    return pagina("Iniciar sesión", contenido)


@app.route("/tareas", methods=["GET"])
def tareas():
    usuario = session.get("usuario")

    if usuario:
        contenido = f"""
        <p>¡Hola, {usuario}! Iniciaste sesión correctamente.</p>
        <p>La API está funcionando correctamente.</p>
        <a class="boton" href="/salir">Cerrar sesión</a>
        """
        return pagina("Bienvenido", contenido)

    contenido = """
    <p>La API está funcionando correctamente.</p>
    <p>Iniciá sesión para ingresar al sistema.</p>
    <a class="boton" href="/login-web">Iniciar sesión</a>
    """
    return pagina("Bienvenido", contenido)


@app.route("/salir")
def salir():
    session.clear()
    flash("Cerraste sesión correctamente.", "")
    return redirect(url_for("login_web"))


if __name__ == "__main__":
    crear_tablas()
    app.run(debug=True)
