import os
import json
from flask import Flask, render_template, request, redirect
import redis

app = Flask(__name__)

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True,
)

NIVELES = ["bajo", "medio", "medio-avanzado", "avanzado"]

STAGE_NAMES = {
    "planta": ["Semilla", "Brote", "Planta", "Árbol joven", "Árbol adulto"],
    "panda":  ["Recién nacido", "Bebé panda", "Cría", "Panda joven", "Panda adulto"],
    "perro":  ["Cachorro", "Perrito", "Perro joven", "Perro adulto", "Guardián"],
    "gato":   ["Gatito", "Minino", "Gato joven", "Gato adulto", "Maestro felino"],
}


def parse_item(raw, index):
    try:
        data = json.loads(raw)
        data["index"] = index
        return data
    except (json.JSONDecodeError, TypeError):
        return {"texto": raw, "tipo": "logro", "nivel": None, "index": index}


def get_stage(p):
    if p == 0:    return 0
    elif p <= 2:  return 1
    elif p <= 5:  return 2
    elif p <= 8:  return 3
    else:         return 4


def get_mascota():
    tipo     = r.get("mascota_tipo")
    progreso = int(r.get("mascota_progreso") or 0)
    t        = tipo or "planta"
    stage    = get_stage(progreso)
    return {
        "tipo":        t,
        "primera_vez": tipo is None,
        "progreso":    progreso,
        "stage":       stage,
        "stage_name":  STAGE_NAMES[t][stage],
    }


def add_mascota():
    progreso = int(r.get("mascota_progreso") or 0)
    progreso += 1
    if progreso >= 10:
        r.set("mascota_progreso", 0)
        tipo = r.get("mascota_tipo") or "planta"
        r.incr(f"mascota_completadas_{tipo}")
        return True
    r.set("mascota_progreso", progreso)
    return False


@app.route("/")
def index():
    raw_items = r.lrange("muro_logros", 0, -1)
    logros  = [parse_item(item, i) for i, item in enumerate(raw_items)]
    mascota = get_mascota()
    completadas = {
        "planta": int(r.get("mascota_completadas_planta") or 0),
        "panda":  int(r.get("mascota_completadas_panda")  or 0),
        "perro":  int(r.get("mascota_completadas_perro")  or 0),
        "gato":   int(r.get("mascota_completadas_gato")   or 0),
    }
    return render_template("index.html", logros=logros, niveles=NIVELES, mascota=mascota, completadas=completadas)


@app.route("/añadir", methods=["POST"])
def añadir():
    texto = request.form.get("logro", "").strip()
    tipo  = request.form.get("tipo", "logro")
    nivel = request.form.get("nivel", "bajo") if tipo == "proceso" else None
    completado = False
    if texto:
        data = {"texto": texto, "tipo": tipo, "nivel": nivel}
        r.lpush("muro_logros", json.dumps(data, ensure_ascii=False))
        if tipo == "logro":
            completado = add_mascota()
    suffix = "&completado=1" if completado else ""
    return redirect(f"/?nuevo={tipo}{suffix}")


@app.route("/actualizar-nivel", methods=["POST"])
def actualizar_nivel():
    index      = request.form.get("index", type=int)
    nuevo_nivel = request.form.get("nivel")
    cambio     = ""
    completado = False
    if index is not None and nuevo_nivel in NIVELES:
        raw = r.lindex("muro_logros", index)
        if raw:
            try:
                data      = json.loads(raw)
                viejo_idx = NIVELES.index(data.get("nivel", "bajo"))
                nuevo_idx = NIVELES.index(nuevo_nivel)
                if nuevo_idx > viejo_idx:
                    cambio = "subio"
                    if nuevo_nivel == "avanzado":
                        completado = add_mascota()
                elif nuevo_idx < viejo_idx:
                    cambio = "bajo"
                data["nivel"] = nuevo_nivel
                r.lset("muro_logros", index, json.dumps(data, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
    suffix = "&completado=1" if completado else ""
    return redirect(f"/?cambio={cambio}{suffix}" if cambio else "/")


@app.route("/elegir-mascota", methods=["POST"])
def elegir_mascota():
    tipo = request.form.get("tipo", "planta")
    if tipo in ("planta", "panda", "perro", "gato"):
        r.set("mascota_tipo", tipo)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
