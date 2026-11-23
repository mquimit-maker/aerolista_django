# ==============================================================
#  persistencia.py · guardar y leer los archivos JSON (carpeta data/)
#    data/vuelos.json    -> lista de vuelos registrados
#    data/reservas.json  -> { "AV101": {"siguiente": 1008, "pasajeros": [ ... ]}, ... }
# ==============================================================
import json
import os
from pathlib import Path

from .lista_pasajeros import ListaPasajeros
from .pasajero import Pasajero
from .vuelo import Vuelo

CARPETA = Path(__file__).resolve().parent.parent / "data"
ARCHIVO_VUELOS = CARPETA / "vuelos.json"
ARCHIVO_RESERVAS = CARPETA / "reservas.json"


def _leer(ruta, defecto):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return defecto


def _escribir(ruta, datos):
    CARPETA.mkdir(exist_ok=True)
    temporal = str(ruta) + ".tmp"
    with open(temporal, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    os.replace(temporal, ruta)      # reemplazo seguro: nunca queda el archivo a medias


# ---------------- vuelos ----------------
def cargar_vuelos():
    return [Vuelo.desde_dict(d) for d in _leer(ARCHIVO_VUELOS, [])]


def guardar_vuelos(vuelos):
    _escribir(ARCHIVO_VUELOS, [v.a_dict() for v in vuelos])


def buscar_vuelo(codigo):
    for v in cargar_vuelos():
        if v.codigo == codigo:
            return v
    return None


# ---------------- reservas (una lista enlazada por vuelo) ----------------
def cargar_reservas(codigo):
    """Retorna (lista_enlazada, siguiente_numero_de_reserva)."""
    datos = _leer(ARCHIVO_RESERVAS, {}).get(codigo, {"siguiente": 1001, "pasajeros": []})
    lista = ListaPasajeros()
    for d in datos["pasajeros"]:
        lista.ingresar(Pasajero.desde_dict(d))
    return lista, datos["siguiente"]


def guardar_reservas(codigo, lista, siguiente):
    todo = _leer(ARCHIVO_RESERVAS, {})
    todo[codigo] = {"siguiente": siguiente,
                    "pasajeros": [p.a_dict() for p in lista.listar()]}
    _escribir(ARCHIVO_RESERVAS, todo)
