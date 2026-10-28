"""Aplicação web do portal Little Garden.

Configuração local: python app.py
Produção: configure APP_ENV=production, LITTLE_GARDEN_SECRET e HTTPS.
"""

import hmac
import os
import re
import secrets
import sqlite3
from datetime import timedelta
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)

APP_ENV = os.environ.get("APP_ENV", "development").strip().lower()
IS_PRODUCTION = APP_ENV == "production"
_secret_key = os.environ.get("LITTLE_GARDEN_SECRET", "").strip()

if IS_PRODUCTION and len(_secret_key) < 32:
    raise RuntimeError(
        "Em produção, defina LITTLE_GARDEN_SECRET com pelo menos 32 caracteres aleatórios."
    )

# Uma chave aleatória temporária é melhor que uma chave fixa conhecida. Em
# desenvolvimento, as sessões são invalidadas quando o processo reinicia.
app.config.update(
    SECRET_KEY=_secret_key or secrets.token_hex(32),
    DATABASE=os.environ.get("LITTLE_GARDEN_DATABASE", str(BASE_DIR / "little_garden.db")),
    SESSION_COOKIE_NAME="little_garden_session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get(
        "COOKIE_SECURE", "1" if IS_PRODUCTION else "0"
    ).strip() == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_REFRESH_EACH_REQUEST=False,
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,
)

if IS_PRODUCTION and not app.config["SESSION_COOKIE_SECURE"]:
    raise RuntimeError("Em produção, configure COOKIE_SECURE=1 e publique o site por HTTPS.")

EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+\Z")


def resolve_database_path() -> Path:
    """Resolve caminhos relativos do banco a partir da pasta do projeto."""
    configured_path = Path(app.config["DATABASE"]).expanduser()
    if not configured_path.is_absolute():
        configured_path = BASE_DIR / configured_path
    return configured_path.resolve()


def get_db() -> sqlite3.Connection:
    """Retorna uma conexão por requisição, fechada ao final dela."""
    if "db" not in g:
        db_path = resolve_database_path()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(str(db_path), timeout=5)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA busy_timeout = 5000")
    return g.db


@app.teardown_appcontext
def close_db(exception=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Cria o esquema necessário sem apagar dados existentes."""
    db_path = resolve_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(db_path), timeout=5)
    try:
        db.execute("PRAGMA journal_mode = WAL")
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL CHECK(length(username) BETWEEN 2 AND 60),
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.commit()
    finally:
        db.close()


def csrf_token() -> str:
    """Gera e mantém um token CSRF imprevisível na sessão do usuário."""
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def protect_post_requests() -> None:
    """Rejeita envios POST sem um token CSRF válido."""
    if request.method == "POST":
        sent_token = request.form.get("_csrf_token", "")
        session_token = session.get("_csrf_token", "")
        if not sent_token or not session_token or not hmac.compare_digest(
            sent_token, session_token
        ):
            abort(
                400,
                description=(
                    "A validação de segurança do formulário falhou. "
                    "Atualize a página e tente novamente."
                ),
            )


@app.after_request
def add_security_headers(response):
    """Aplica cabeçalhos defensivos às respostas do site."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")
    response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    response.headers.setdefault(
        "Permissions-Policy", "camera=(), microphone=(), geolocation=()"
    )
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; script-src 'self'; "
        "connect-src 'self'; object-src 'none'; base-uri 'self'; "
        "frame-ancestors 'none'; form-action 'self'",
    )
    if app.config["SESSION_COOKIE_SECURE"]:
        response.headers.setdefault(
            "Strict-Transport-Security", "max-age=31536000"
        )
    if request.endpoint in {"perfil", "login", "cadastro"}:
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
    return response


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
        user = get_db().execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (session["user_id"],),
        ).fetchone()
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

        if not 2 <= len(username) <= 60 or any(ord(char) < 32 for char in username):
            flash("O nome precisa ter entre 2 e 60 caracteres válidos.", "error")
        elif len(email) > 254 or not EMAIL_PATTERN.fullmatch(email):
            flash("Informe um e-mail válido.", "error")
        elif len(password) < 12:
            flash("A senha precisa ter pelo menos 12 caracteres.", "error")
        elif len(password) > 256:
            flash("A senha é muito longa.", "error")
        elif password != confirm:
            flash("As senhas não coincidem.", "error")
        else:
            try:
                db = get_db()
                cursor = db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db.commit()
                # Evita preservar dados de uma sessão anterior após autenticação.
                session.clear()
                session.permanent = True
                session["user_id"] = cursor.lastrowid
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
        user = get_db().execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session.permanent = True
            session["user_id"] = user["id"]
            flash("Que bom ter você de volta!", "success")
            return redirect(url_for("perfil"))
        # Mensagem única evita revelar se determinado e-mail está cadastrado.
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
    user = get_db().execute(
        "SELECT id, username, email, created_at FROM users WHERE id = ?",
        (session["user_id"],),
    ).fetchone()
    if user is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template("perfil.html", user=user)


@app.errorhandler(400)
def bad_request(error):
    message = getattr(error, "description", "A solicitação não pôde ser processada.")
    return render_template("400.html", message=message), 400


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    # Não exibe detalhes internos, caminhos ou consultas SQL ao visitante.
    return render_template("500.html"), 500


# Inicialização idempotente: não remove nem recria os dados dos usuários.
with app.app_context():
    init_db()


if __name__ == "__main__":
    # O modo debug exige ativação explícita e nunca é ligado por padrão.
    app.run(debug=(not IS_PRODUCTION and os.environ.get("FLASK_DEBUG") == "1"))
