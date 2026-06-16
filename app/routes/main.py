from flask import Blueprint, render_template
from extensions import r
from config import NIVELES
from services.pet_service import get_pet
from services.achievement_service import parse_item

bp = Blueprint("main", __name__)


# esta es la página de inicio, la que carga todo lo que se ve / this is the home page, it loads everything you see
@bp.route("/")
def index():
    raw_items = r.lrange("muro_logros", 0, -1)  # trae todos los logros guardados en Redis / fetches all achievements stored in Redis
    achievements = [parse_item(item, i) for i, item in enumerate(raw_items)]  # los convierte uno por uno a diccionarios / converts them one by one to dictionaries
    pet = get_pet()  # trae el estado actual de la mascota / fetches the current state of the pet
    completed = {
        # cuenta cuántas veces se completó cada mascota / counts how many times each pet was completed
        "planta": int(r.get("mascota_completadas_planta") or 0),
        "panda":  int(r.get("mascota_completadas_panda")  or 0),
        "perro":  int(r.get("mascota_completadas_perro")  or 0),
        "gato":   int(r.get("mascota_completadas_gato")   or 0),
    }
    # manda todo eso al HTML para que se muestre / sends all that to the HTML to be displayed
    return render_template(
        "index.html",
        logros=achievements,
        niveles=NIVELES,
        mascota=pet,
        completadas=completed,
    )
