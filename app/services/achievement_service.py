import json


# convierte el texto guardado en Redis en un diccionario usable / turns the text stored in Redis into a usable dictionary
def parse_item(raw, index):
    try:
        data = json.loads(raw)
        data["index"] = index  # le agrega su posición en la lista / adds its position in the list
        return data
    except (json.JSONDecodeError, TypeError):
        # si algo falla, devuelve un logro básico con el texto crudo / if something fails, returns a basic achievement with the raw text
        return {"texto": raw, "tipo": "logro", "nivel": None, "index": index}
