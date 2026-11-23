# AeroLista · Reserva de vuelos con Django

Proyecto de Estructura de Datos (UNEMI). Django + HTML/CSS/Bootstrap + lista enlazada propia + archivos JSON.

## Cómo ejecutarlo
```
python -m venv venv
venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py runserver
```
Abre http://127.0.0.1:8000  (necesita internet para cargar Bootstrap).

## Estructura
- `config/`  configuración de Django (settings.py, urls.py)
- `reservas/views.py`  la lógica de cada página
- `reservas/lista_pasajeros.py`  lista enlazada con los 9 métodos
- `reservas/persistencia.py`  lee y guarda los JSON
- `reservas/templates/reservas/`  páginas HTML con Bootstrap
- `data/vuelos.json` y `data/reservas.json`  datos persistentes
- `prueba_consola.py`  prueba los 9 métodos sin Django: `python prueba_consola.py`
