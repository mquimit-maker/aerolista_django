# ==============================================================
#  lista_pasajeros.py · LISTA ENLAZADA de pasajeros (cada vuelo tiene la suya)
# --------------------------------------------------------------
#        head
#         |
#         v
#    +----------+---+    +----------+---+    +----------+---+
#    | #1001    | o-+--->| #1002    | o-+--->| #1003    | o-+---> None
#    | Ana 1A   |   |    | Diana 3C |   |    | Luis 7D  |   |
#    +----------+---+    +----------+---+    +----------+---+
#       data    next        data    next        data    next
#
#  REGLAS: recorrer SIEMPRE con  actual = self.head / while actual is not None /
#  actual = actual.next · no convertir la lista en list de Python (salvo el
#  resultado de listar y filtrar_por_clase) · sin print() ni input().
# ==============================================================

from .pasajero import Pasajero


class Nodo:
    """Un vagón del tren: lleva un pasajero (data) y el enganche al siguiente (next)."""

    def __init__(self, data):
        self.data = data     # el Pasajero
        self.next = None     # al nacer no apunta a nadie


class ListaPasajeros:
    def __init__(self):
        self.head = None     # primer nodo (None = avión vacío)
        self.cantidad = 0    # cuántas reservas hay

    # ----------------------------------------------------------
    # ingresar: agrega al FINAL (orden de llegada)
    # ----------------------------------------------------------
    def ingresar(self, pasajero):
        nuevo = Nodo(pasajero)
        if self.head is None:                 # lista vacía: el nuevo es la cabeza
            self.head = nuevo
        else:
            actual = self.head
            while actual.next is not None:    # avanzo hasta el ÚLTIMO vagón
                actual = actual.next
            actual.next = nuevo               # el último apunta al nuevo
        self.cantidad = self.cantidad + 1
        return True

    # ----------------------------------------------------------
    # 1. esta_vacia: si la cabeza no apunta a nadie, no hay reservas
    # ----------------------------------------------------------
    def esta_vacia(self):
        return self.head is None              # la comparación ya es True/False

    # ----------------------------------------------------------
    # 2. longitud: ya llevamos la cuenta en self.cantidad (no se recorre)
    # ----------------------------------------------------------
    def longitud(self):
        return self.cantidad

    # ----------------------------------------------------------
    # 3. listar: recorrido + acumulador. Guarda actual.data (el Pasajero)
    # ----------------------------------------------------------
    def listar(self):
        resultado = []                        # la "caja de envío"
        actual = self.head                    # el dedo en la cabeza
        while actual is not None:
            resultado.append(actual.data)     # agrego el PASAJERO, no el nodo
            actual = actual.next              # avanzo el dedo
        return resultado

    # ----------------------------------------------------------
    # 4. buscar: búsqueda lineal por número de reserva
    # ----------------------------------------------------------
    def buscar(self, numero):
        actual = self.head
        while actual is not None:
            if actual.data.numero == numero:  # data es un Pasajero: comparo su atributo
                return actual.data
            actual = actual.next
        return None                           # recorrí todo y no apareció

    # ----------------------------------------------------------
    # 5. buscar_por_asiento: mismo patrón, otro atributo
    # ----------------------------------------------------------
    def buscar_por_asiento(self, asiento):
        actual = self.head
        while actual is not None:
            if actual.data.asiento == asiento:
                return actual.data
            actual = actual.next
        return None

    # ----------------------------------------------------------
    # 6. buscar_por_cedula: igual, la cédula es str ("0912345678")
    # ----------------------------------------------------------
    def buscar_por_cedula(self, cedula):
        actual = self.head
        while actual is not None:
            if actual.data.cedula == cedula:
                return actual.data
            actual = actual.next
        return None

    # ----------------------------------------------------------
    # 7. modificar: reutiliza buscar. Como buscar retorna EL MISMO objeto que
    #    está dentro del nodo, al cambiarle los atributos cambia en la lista.
    # ----------------------------------------------------------
    def modificar(self, numero, nuevo_nombre, nueva_edad, nuevo_asiento):
        pasajero = self.buscar(numero)
        if pasajero is None:
            return False
        pasajero.nombre = nuevo_nombre
        pasajero.edad = nueva_edad
        pasajero.asiento = nuevo_asiento
        return True

    # ----------------------------------------------------------
    # 8. eliminar: 4 casos (A vacía · B cabeza · C medio/final · D no existe)
    # ----------------------------------------------------------
    def eliminar(self, numero):
        # Caso A: lista vacía
        if self.head is None:
            return None

        # Caso B: es la cabeza -> la cabeza pasa al segundo vagón
        if self.head.data.numero == numero:
            quitado = self.head
            self.head = self.head.next
            self.cantidad = self.cantidad - 1
            return quitado.data

        # Caso C/D: camino con "anterior" mirando UN VAGÓN ADELANTE
        anterior = self.head
        while anterior.next is not None and anterior.next.data.numero != numero:
            anterior = anterior.next

        # Caso D: llegué al último y no lo encontré
        if anterior.next is None:
            return None

        # Caso C: anterior.next es el que sobra; el anterior "se salta" ese nodo
        quitado = anterior.next
        anterior.next = quitado.next
        self.cantidad = self.cantidad - 1
        return quitado.data

    # ----------------------------------------------------------
    # 9. filtrar_por_clase: listar + un if
    # ----------------------------------------------------------
    def filtrar_por_clase(self, clase):
        resultado = []
        actual = self.head
        while actual is not None:
            if actual.data.clase() == clase:
                resultado.append(actual.data)
            actual = actual.next
        return resultado
