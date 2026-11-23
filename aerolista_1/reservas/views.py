# ==============================================================
#  views.py · las "vistas" de Django (lo que en Flask era app.py)
#  Cada vista recibe un request y retorna una página (render) o redirige.
# ==============================================================
import re

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import persistencia
from .pasajero import Pasajero
from .vuelo import Vuelo


# ---------------- funciones de apoyo ----------------
def estadisticas(vuelo, lista):
    """Ocupación del vuelo y color del semáforo."""
    ocupados = lista.longitud()
    capacidad = vuelo.capacidad()
    porcentaje = round(ocupados * 100 / capacidad)
    color = "success" if porcentaje < 50 else ("warning" if porcentaje < 80 else "danger")
    return {"ocupados": ocupados, "libres": capacidad - ocupados,
            "capacidad": capacidad, "porcentaje": porcentaje, "color": color}


def construir_mapa(vuelo, ocupados, editando):
    """Arma las filas de asientos del avión. `ocupados` es {"7D": Pasajero}."""
    mapa = []
    for fila in range(1, vuelo.filas + 1):
        asientos = []
        for letra in Vuelo.COLUMNAS:
            codigo = f"{fila}{letra}"
            dueno = ocupados.get(codigo)
            mio = editando is not None and dueno is not None and dueno.numero == editando.numero
            asientos.append({"codigo": codigo, "dueno": dueno, "mio": mio,
                             "ocupado": dueno is not None and not mio,
                             "ejecutiva": fila <= Pasajero.FILAS_EJECUTIVA})
        mapa.append({"numero": fila, "izq": asientos[:3], "der": asientos[3:]})
    return mapa


def validar_datos(vuelo, nombre, edad_txt, asiento):
    """Retorna (edad, mensaje_de_error). Si todo está bien, el error es None."""
    if not nombre:
        return None, "El nombre es obligatorio."
    if not edad_txt.isdigit() or not (0 <= int(edad_txt) <= 120):
        return None, "La edad debe ser un número entre 0 y 120."
    m = re.fullmatch(r"(\d{1,2})([A-F])", asiento)
    if not m or not (1 <= int(m.group(1)) <= vuelo.filas):
        return None, "Debes elegir un asiento válido en el mapa."
    return int(edad_txt), None


def vuelo_o_redirigir(request, codigo):
    vuelo = persistencia.buscar_vuelo(codigo)
    if vuelo is None:
        messages.error(request, f"No existe el vuelo {codigo}.")
    return vuelo


# ---------------- vistas ----------------
def inicio(request):
    """Consulta de vuelos (con búsqueda por origen, destino y fecha) + formulario de registro."""
    origen = request.GET.get("origen", "").strip().lower()
    destino = request.GET.get("destino", "").strip().lower()
    fecha = request.GET.get("fecha", "").strip()

    filas = []
    for v in persistencia.cargar_vuelos():
        if origen and origen not in v.origen.lower():
            continue
        if destino and destino not in v.destino.lower():
            continue
        if fecha and fecha != v.fecha:
            continue
        lista, _ = persistencia.cargar_reservas(v.codigo)
        filas.append({"vuelo": v, **estadisticas(v, lista)})

    return render(request, "reservas/inicio.html", {
        "filas": filas,
        "filtros": {"origen": request.GET.get("origen", ""),
                    "destino": request.GET.get("destino", ""), "fecha": fecha},
    })


@require_POST
def registrar_vuelo(request):
    codigo = request.POST.get("codigo", "").strip().upper()
    origen = request.POST.get("origen", "").strip()
    destino = request.POST.get("destino", "").strip()
    fecha = request.POST.get("fecha", "").strip()
    hora = request.POST.get("hora", "").strip()
    filas_txt = request.POST.get("filas", "").strip()

    if not (codigo and origen and destino and fecha and hora):
        messages.error(request, "Completa todos los campos del vuelo.")
    elif not filas_txt.isdigit() or not (1 <= int(filas_txt) <= 30):
        messages.error(request, "Las filas deben ser un número entre 1 y 30.")
    elif persistencia.buscar_vuelo(codigo) is not None:
        messages.error(request, f"Ya existe un vuelo con el código {codigo}.")
    elif origen.lower() == destino.lower():
        messages.error(request, "El origen y el destino no pueden ser iguales.")
    else:
        vuelos = persistencia.cargar_vuelos()
        vuelos.append(Vuelo(codigo, origen, destino, fecha, hora, int(filas_txt)))
        persistencia.guardar_vuelos(vuelos)
        messages.success(request, f"Vuelo {codigo} registrado ({origen} → {destino}).")
    return redirect("inicio")


def vuelo_detalle(request, codigo):
    """Mapa de asientos, formulario de reserva/modificación, búsqueda y listado."""
    vuelo = vuelo_o_redirigir(request, codigo)
    if vuelo is None:
        return redirect("inicio")

    lista, _ = persistencia.cargar_reservas(codigo)
    todos = lista.listar()
    ocupados = {p.asiento: p for p in todos}

    # ¿modificando una reserva? (?editar=1003)
    editando = None
    if request.GET.get("editar", "").isdigit():
        editando = lista.buscar(int(request.GET["editar"]))

    # búsqueda (?tipo=numero|cedula|asiento&q=...)
    tipo = request.GET.get("tipo", "numero")
    q = request.GET.get("q", "").strip()
    buscado, resultado = bool(q), None
    if q:
        if tipo == "numero" and q.isdigit():
            resultado = lista.buscar(int(q))
        elif tipo == "cedula":
            resultado = lista.buscar_por_cedula(q)
        elif tipo == "asiento":
            resultado = lista.buscar_por_asiento(q.upper())

    # filtro por clase (?clase=Ejecutiva|Económica)
    clase = request.GET.get("clase", "")
    pasajeros = lista.filtrar_por_clase(clase) if clase in ("Ejecutiva", "Económica") else todos

    return render(request, "reservas/vuelo.html", {
        "vuelo": vuelo, "mapa": construir_mapa(vuelo, ocupados, editando),
        "stats": estadisticas(vuelo, lista), "pasajeros": pasajeros, "todos": todos,
        "editando": editando, "buscado": buscado, "resultado": resultado,
        "tipo": tipo, "q": q, "clase": clase,
    })


@require_POST
def reservar(request, codigo):
    vuelo = vuelo_o_redirigir(request, codigo)
    if vuelo is None:
        return redirect("inicio")
    lista, siguiente = persistencia.cargar_reservas(codigo)

    nombre = request.POST.get("nombre", "").strip()
    cedula = request.POST.get("cedula", "").strip()
    asiento = request.POST.get("asiento", "").strip().upper()
    edad, error = validar_datos(vuelo, nombre, request.POST.get("edad", "").strip(), asiento)

    if error is None and not (cedula.isdigit() and len(cedula) == 10):
        error = "La cédula debe tener exactamente 10 dígitos."
    if error is None and lista.buscar_por_asiento(asiento) is not None:   # no vender 2 veces
        error = f"El asiento {asiento} ya está reservado."
    if error is None and lista.buscar_por_cedula(cedula) is not None:     # 1 asiento por persona
        error = f"La cédula {cedula} ya tiene una reserva en este vuelo."

    if error:
        messages.error(request, error)
    else:
        lista.ingresar(Pasajero(siguiente, nombre, cedula, edad, asiento))
        persistencia.guardar_reservas(codigo, lista, siguiente + 1)
        messages.success(request, f"Reserva #{siguiente} creada: {nombre}, asiento {asiento}.")
    return redirect("vuelo", codigo=codigo)


@require_POST
def modificar(request, codigo, numero):
    vuelo = vuelo_o_redirigir(request, codigo)
    if vuelo is None:
        return redirect("inicio")
    lista, siguiente = persistencia.cargar_reservas(codigo)

    nombre = request.POST.get("nombre", "").strip()
    asiento = request.POST.get("asiento", "").strip().upper()
    edad, error = validar_datos(vuelo, nombre, request.POST.get("edad", "").strip(), asiento)

    if error is None:
        otro = lista.buscar_por_asiento(asiento)
        if otro is not None and otro.numero != numero:   # ocupado por OTRA persona
            error = f"El asiento {asiento} ya está reservado."

    if error is None and not lista.modificar(numero, nombre, edad, asiento):
        error = f"No existe la reserva #{numero}."

    if error:
        messages.error(request, error)
        return redirect(f"/vuelos/{codigo}/?editar={numero}")
    persistencia.guardar_reservas(codigo, lista, siguiente)
    messages.success(request, f"Reserva #{numero} modificada.")
    return redirect("vuelo", codigo=codigo)


@require_POST
def eliminar(request, codigo, numero):
    vuelo = vuelo_o_redirigir(request, codigo)
    if vuelo is None:
        return redirect("inicio")
    lista, siguiente = persistencia.cargar_reservas(codigo)
    quitado = lista.eliminar(numero)
    if quitado is None:
        messages.error(request, f"No existe la reserva #{numero}.")
    else:
        persistencia.guardar_reservas(codigo, lista, siguiente)
        messages.success(request, f"Reserva #{numero} cancelada: el asiento {quitado.asiento} quedó libre.")
    return redirect("vuelo", codigo=codigo)
