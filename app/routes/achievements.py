import json
from flask import Blueprint, request, redirect
from extensions import r
from config import NIVELES
from services.pet_service import advance_pet

bp = Blueprint("achievements", __name__)


# edita el texto de un logro o proceso existente / edits the text of an existing achievement or process
@bp.route("/editar", methods=["POST"])
def edit():
    index = request.form.get("index", type=int)
    new_text = request.form.get("texto", "").strip()
    if index is not None and new_text:
        raw = r.lindex("muro_logros", index)  # busca el item por su posición / finds the item by its position
        if raw:
            try:
                data = json.loads(raw)
                data["texto"] = new_text  # reemplaza solo el texto, el resto queda igual / replaces only the text, everything else stays
                r.lset("muro_logros", index, json.dumps(data, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError):
                pass
    return redirect("/")


# elimina un logro o proceso de la lista / removes an achievement or process from the list
@bp.route("/eliminar", methods=["POST"])
def delete():
    index = request.form.get("index", type=int)
    if index is not None:
        r.lset("muro_logros", index, "__deleted__")   # lo marca con un valor temporal / marks it with a temporary value
        r.lrem("muro_logros", 1, "__deleted__")        # luego lo borra de verdad / then removes it for real
    return redirect("/")


# esto recibe el formulario y guarda el logro o proceso que escribió el usuario / receives the form and saves the achievement or process the user wrote
@bp.route("/añadir", methods=["POST"])
def add():
    text = request.form.get("logro", "").strip()
    kind = request.form.get("tipo", "logro")
    level = request.form.get("nivel", "bajo") if kind == "proceso" else None
    completed = False
    if text:
        data = {"texto": text, "tipo": kind, "nivel": level}
        r.lpush("muro_logros", json.dumps(data, ensure_ascii=False))  # lo mete al inicio de la lista en Redis / pushes it to the front of the list in Redis
        if kind == "logro":
            completed = advance_pet()  # si es un logro, la mascota sube de progreso / if it's an achievement, the pet gains progress
    suffix = "&completado=1" if completed else ""
    return redirect(f"/?nuevo={kind}{suffix}")


# esto cambia el nivel de un proceso existente (ej: de "bajo" a "medio") / changes the level of an existing process (e.g. from "bajo" to "medio")
@bp.route("/actualizar-nivel", methods=["POST"])
def update_level():
    index = request.form.get("index", type=int)
    new_level = request.form.get("nivel")
    change = ""
    completed = False
    if index is not None and new_level in NIVELES:
        raw = r.lindex("muro_logros", index)  # busca ese logro por su posición / finds that achievement by its position
        if raw:
            try:
                data = json.loads(raw)
                old_idx = NIVELES.index(data.get("nivel", "bajo"))
                new_idx = NIVELES.index(new_level)
                # compara el nivel viejo con el nuevo para saber si subió o bajó / compares old and new level to know if it went up or down
                if new_idx > old_idx:
                    change = "subio"
                    if new_level == "avanzado":
                        completed = advance_pet()  # llegar a "avanzado" también sube a la mascota / reaching "avanzado" also boosts the pet
                elif new_idx < old_idx:
                    change = "bajo"
                data["nivel"] = new_level
                r.lset("muro_logros", index, json.dumps(data, ensure_ascii=False))  # guarda el cambio en Redis / saves the change to Redis
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
    suffix = "&completado=1" if completed else ""
    return redirect(f"/?cambio={change}{suffix}" if change else "/")
