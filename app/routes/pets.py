from flask import Blueprint, request, redirect
from extensions import r

bp = Blueprint("pets", __name__)


# guarda en Redis qué mascota eligió el usuario / saves to Redis which pet the user chose
@bp.route("/elegir-mascota", methods=["POST"])
def choose():
    pet_type = request.form.get("tipo", "planta")
    if pet_type in ("planta", "panda", "perro", "gato"):  # solo acepta mascotas válidas / only accepts valid pets
        r.set("mascota_tipo", pet_type)
    return redirect("/")
