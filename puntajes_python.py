import json
import os

RUTA_RANKING = "ranking.json"
MAX_RANKING = 5  # top 5 jugadores

def cargar_ranking():
    if not os.path.exists(RUTA_RANKING):
        return []
    with open(RUTA_RANKING, "r") as archivo:
        return json.load(archivo)

def guardar_ranking(ranking):
    with open(RUTA_RANKING, "w") as archivo:
        json.dump(ranking, archivo, indent=4)

def actualizar_ranking(nombre, puntaje):
    ranking = cargar_ranking()
    ranking.append({"nombre": nombre, "puntaje": puntaje})
    ranking.sort(key=lambda x: x["puntaje"], reverse=True)
    ranking = ranking[:MAX_RANKING]  # solo top 5
    guardar_ranking(ranking)
    return ranking
