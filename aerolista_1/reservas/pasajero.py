# ==============================================================
#  pasajero.py · la clase Pasajero (los datos de una reserva)
# ==============================================================

class Pasajero:
    FILAS_EJECUTIVA = 3   # las filas 1, 2 y 3 son clase Ejecutiva

    def __init__(self, numero, nombre, cedula, edad, asiento):
        self.numero = numero      # int  · número de reserva (1001, 1002...)
        self.nombre = nombre      # str
        self.cedula = cedula      # str  · texto de 10 dígitos (conserva el 0 inicial)
        self.edad = edad          # int
        self.asiento = asiento    # str  · "7D" (fila + letra)

    def fila(self):
        """De '10B' retorna 10."""
        return int(self.asiento[:-1])

    def clase(self):
        return "Ejecutiva" if self.fila() <= Pasajero.FILAS_EJECUTIVA else "Económica"

    def es_menor(self):
        return self.edad < 18

    # --- para guardar y leer del JSON ---
    def a_dict(self):
        return {"numero": self.numero, "nombre": self.nombre, "cedula": self.cedula,
                "edad": self.edad, "asiento": self.asiento}

    @staticmethod
    def desde_dict(d):
        return Pasajero(d["numero"], d["nombre"], d["cedula"], d["edad"], d["asiento"])
