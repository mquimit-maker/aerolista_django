# ==============================================================
#  vuelo.py · la clase Vuelo (datos de cada vuelo registrado)
# ==============================================================

class Vuelo:
    COLUMNAS = "ABCDEF"   # 6 asientos por fila: ABC | pasillo | DEF

    def __init__(self, codigo, origen, destino, fecha, hora, filas):
        self.codigo = codigo      # "AV101"
        self.origen = origen
        self.destino = destino
        self.fecha = fecha        # "2026-11-30"
        self.hora = hora          # "08:30"
        self.filas = filas        # cuántas filas tiene el avión

    def capacidad(self):
        return self.filas * len(Vuelo.COLUMNAS)

    def a_dict(self):
        return {"codigo": self.codigo, "origen": self.origen, "destino": self.destino,
                "fecha": self.fecha, "hora": self.hora, "filas": self.filas}

    @staticmethod
    def desde_dict(d):
        return Vuelo(d["codigo"], d["origen"], d["destino"], d["fecha"], d["hora"], d["filas"])
