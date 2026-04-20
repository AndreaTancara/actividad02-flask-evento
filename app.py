from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():

    conn = sqlite3.connect("database.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS participantes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        telefono TEXT,
        fecha_registro TEXT

    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/guardar", methods=["POST"])
def guardar():

    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    conn = sqlite3.connect("database.db")

    conn.execute("""
    INSERT INTO participantes(nombre,email,telefono,fecha_registro)
    VALUES(?,?,?,?)
    """,(nombre,email,telefono,fecha))

    conn.commit()
    conn.close()

    return redirect("/participantes")


@app.route("/participantes")
def participantes():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    participantes = conn.execute("SELECT * FROM participantes").fetchall()

    return render_template("participantes.html",participantes=participantes)


@app.route("/eliminar/<int:id>")
def eliminar(id):

    conn = sqlite3.connect("database.db")

    conn.execute("DELETE FROM participantes WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/participantes")


@app.route("/editar/<int:id>")
def editar(id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    participante = conn.execute("SELECT * FROM participantes WHERE id=?",(id,)).fetchone()

    return render_template("editar.html",participante=participante)


@app.route("/actualizar",methods=["POST"])
def actualizar():

    id = request.form["id"]
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    conn = sqlite3.connect("database.db")

    conn.execute("""
    UPDATE participantes
    SET nombre=?,email=?,telefono=?,fecha_registro=?
    WHERE id=?
    """,(nombre,email,telefono,fecha,id))

    conn.commit()
    conn.close()

    return redirect("/participantes")


if __name__ == "__main__":
    app.run(debug=True)