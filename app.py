from flask import Flask, render_template, request, jsonify, session
import psycopg
from psycopg.rows import dict_row
import os, uuid
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ajudajf-secret-2024")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ajudajf2024")
DATABASE_URL   = os.environ.get("DATABASE_URL", "")

# ── banco ──────────────────────────────────────────────────────────────────────

def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pontos (
                id          TEXT PRIMARY KEY,
                nome        TEXT NOT NULL,
                endereco    TEXT NOT NULL,
                latitude    DOUBLE PRECISION NOT NULL,
                longitude   DOUBLE PRECISION NOT NULL,
                responsavel TEXT DEFAULT '',
                telefone    TEXT DEFAULT '',
                horario     TEXT DEFAULT '',
                itens       TEXT DEFAULT '',
                ativo       BOOLEAN DEFAULT TRUE,
                criado_em   TIMESTAMP DEFAULT NOW()
            )
        """)
        row = conn.execute("SELECT COUNT(*) AS n FROM pontos").fetchone()
        if row["n"] == 0:
            pontos_iniciais = [
                (str(uuid.uuid4()), "Centro de Arrecadação – Prefeitura",
                 "Av. Brasil, 2001 - Centro, Juiz de Fora - MG",
                 -21.7622, -43.3496, "Defesa Civil Municipal",
                 "(32) 3690-8000", "Seg a Dom: 08h às 20h",
                 "Roupas, alimentos não perecíveis, água, cobertores"),
                (str(uuid.uuid4()), "Ginásio Poliesportivo – São Mateus",
                 "R. Halfeld, 150 - São Mateus, Juiz de Fora - MG",
                 -21.7558, -43.3520, "Bombeiros Voluntários",
                 "(32) 3215-4500", "24 horas",
                 "Colchões, roupas de cama, alimentos, medicamentos"),
                (str(uuid.uuid4()), "Igreja N. Sra. Aparecida – Cascatinha",
                 "R. Cascatinha, 400 - Cascatinha, Juiz de Fora - MG",
                 -21.7480, -43.3610, "Pastoral Social",
                 "(32) 3231-1200", "Seg a Sáb: 07h às 18h",
                 "Alimentos, água mineral, artigos de higiene"),
            ]
            conn.executemany("""
                INSERT INTO pontos
                  (id,nome,endereco,latitude,longitude,responsavel,telefone,horario,itens)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, pontos_iniciais)

try:
    init_db()
    print("[OK] Banco inicializado com sucesso.")
except Exception as e:
    print(f"[ERRO] init_db falhou: {e}")

# ── auth ───────────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return jsonify({"error": "Não autorizado"}), 401
        return f(*args, **kwargs)
    return decorated

# ── error handler global ───────────────────────────────────────────────────────

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"[ERRO] {e}")
    return jsonify({"error": str(e)}), 500

# ── rotas públicas ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/pontos")
def api_pontos():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM pontos WHERE ativo=TRUE ORDER BY criado_em"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

# ── auth ───────────────────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    if data.get("senha") == ADMIN_PASSWORD:
        session["admin"] = True
        return jsonify({"ok": True})
    return jsonify({"error": "Senha incorreta"}), 401

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop("admin", None)
    return jsonify({"ok": True})

@app.route("/api/me")
def api_me():
    return jsonify({"admin": bool(session.get("admin"))})

# ── rotas admin ────────────────────────────────────────────────────────────────

@app.route("/api/admin/pontos", methods=["GET"])
@login_required
def admin_lista():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM pontos ORDER BY criado_em DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/admin/pontos", methods=["POST"])
@login_required
def admin_criar():
    d = request.get_json()
    if not d.get("nome") or not d.get("endereco"):
        return jsonify({"error": "Nome e endereço são obrigatórios"}), 400
    try:
        lat = float(d["latitude"])
        lon = float(d["longitude"])
    except (KeyError, ValueError):
        return jsonify({"error": "Coordenadas inválidas"}), 400

    pid = str(uuid.uuid4())
    with get_db() as conn:
        conn.execute("""
            INSERT INTO pontos
              (id, nome, endereco, latitude, longitude,
               responsavel, telefone, horario, itens)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (pid, d["nome"], d["endereco"], lat, lon,
              d.get("responsavel", ""), d.get("telefone", ""),
              d.get("horario", ""),    d.get("itens", "")))
    return jsonify({"ok": True, "id": pid}), 201

@app.route("/api/admin/pontos/<pid>/toggle", methods=["POST"])
@login_required
def admin_toggle(pid):
    with get_db() as conn:
        conn.execute(
            "UPDATE pontos SET ativo = NOT ativo WHERE id = %s", (pid,)
        )
    return jsonify({"ok": True})

@app.route("/api/admin/pontos/<pid>", methods=["DELETE"])
@login_required
def admin_deletar(pid):
    with get_db() as conn:
        conn.execute("DELETE FROM pontos WHERE id = %s", (pid,))
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
