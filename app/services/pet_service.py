from extensions import r
from config import STAGE_NAMES


# convierte el progreso (0 al 10) en una de las 5 etapas visuales / turns progress (0 to 10) into one of 5 visual stages
def get_stage(progress):
    if progress == 0:    return 0
    elif progress <= 2:  return 1
    elif progress <= 5:  return 2
    elif progress <= 8:  return 3
    else:                return 4


# lee toda la info de la mascota desde Redis y la devuelve lista para usar / reads all pet info from Redis and returns it ready to use
def get_pet():
    pet_type = r.get("mascota_tipo")
    progress = int(r.get("mascota_progreso") or 0)
    t = pet_type or "planta"
    stage = get_stage(progress)
    return {
        "tipo":        t,
        "primera_vez": pet_type is None,  # si no hay tipo guardado, es la primera vez / if no type saved, it's the first visit
        "progreso":    progress,
        "stage":       stage,
        "stage_name":  STAGE_NAMES[t][stage],
    }


# le sube 1 de progreso a la mascota; si llega a 10 la "completa" y empieza de cero / adds 1 progress to the pet; if it hits 10 it "completes" and resets
def advance_pet():
    progress = int(r.get("mascota_progreso") or 0)
    progress += 1
    if progress >= 10:
        r.set("mascota_progreso", 0)
        pet_type = r.get("mascota_tipo") or "planta"
        r.incr(f"mascota_completadas_{pet_type}")  # suma 1 al contador de completadas de esa mascota / adds 1 to that pet's completion counter
        return True
    r.set("mascota_progreso", progress)
    return False
