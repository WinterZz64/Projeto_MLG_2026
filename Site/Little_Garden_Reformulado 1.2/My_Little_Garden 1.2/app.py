import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("LITTLE_GARDEN_SECRET", "troque-esta-chave-antes-de-publicar-9f4c7d2a")
app.config["DATABASE"] = os.path.join(BASE_DIR, "little_garden.db")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    db.close()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Entre na sua conta para acessar essa página.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_user():
    if "user_id" in session:
        user = get_db().execute("SELECT id, username, email FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    else:
        user = None
    return {"current_user": user}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/mecanicas")
def mecanicas():
    return render_template("mecanicas.html")

@app.route("/personagens")
def personagens():
    return render_template("personagens.html")

@app.route("/ambiental")
def ambiental():
    return render_template("ambiental.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if len(username) < 2:
            flash("Seu nome precisa ter pelo menos 2 caracteres.", "error")
        elif "@" not in email or "." not in email.split("@")[-1]:
            flash("Informe um e-mail válido.", "error")
        elif len(password) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres.", "error")
        elif password != confirm:
            flash("As senhas não coincidem.", "error")
        else:
            try:
                db = get_db()
                cur = db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password))
                )
                db.commit()
                session.clear()
                session["user_id"] = cur.lastrowid
                flash("Conta criada! Sua jornada começa agora.", "success")
                return redirect(url_for("perfil"))
            except sqlite3.IntegrityError:
                flash("Já existe uma conta com esse e-mail.", "error")
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT id, password_hash FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            flash("Que bom ter você de volta!", "success")
            return redirect(url_for("perfil"))
        flash("E-mail ou senha incorretos.", "error")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("index"))

@app.route("/perfil")
@login_required
def perfil():
    user = get_db().execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    if user is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template("perfil.html", user=user)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
