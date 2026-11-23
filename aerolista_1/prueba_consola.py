# ==============================================================
#  prueba_consola.py · prueba los 9 métodos SIN abrir Django
#  Ejecuta (desde esta carpeta):  python prueba_consola.py
# ==============================================================
from reservas.lista_pasajeros import ListaPasajeros
from reservas.pasajero import Pasajero


def comprobar(titulo, obtenido, esperado):
    estado = "✅" if obtenido == esperado else "❌"
    print(f"{estado} {titulo}: obtuvo {obtenido!r} (esperado {esperado!r})")


lista = ListaPasajeros()
comprobar("1. esta_vacia (vacía)", lista.esta_vacia(), True)
comprobar("2. longitud (vacía)", lista.longitud(), 0)
comprobar("3. listar (vacía)", lista.listar(), [])
comprobar("8. eliminar (vacía, caso A)", lista.eliminar(1001), None)

lista.ingresar(Pasajero(1001, "Ana",   "0911111111", 28, "1A"))
lista.ingresar(Pasajero(1002, "Diana", "0922222222", 35, "3C"))
lista.ingresar(Pasajero(1003, "Luis",  "0933333333", 41, "7D"))
lista.ingresar(Pasajero(1004, "Beto",  "0934567890", 16, "7E"))

comprobar("1. esta_vacia", lista.esta_vacia(), False)
comprobar("2. longitud", lista.longitud(), 4)
comprobar("3. listar (orden)", [p.nombre for p in lista.listar()], ["Ana", "Diana", "Luis", "Beto"])
comprobar("4. buscar 1003", lista.buscar(1003).nombre, "Luis")
comprobar("4. buscar 9999", lista.buscar(9999), None)
comprobar("5. buscar_por_asiento 7E", lista.buscar_por_asiento("7E").nombre, "Beto")
comprobar("5. buscar_por_asiento 9Z", lista.buscar_por_asiento("9Z"), None)
comprobar("6. buscar_por_cedula (con cero)", lista.buscar_por_cedula("0934567890").nombre, "Beto")
comprobar("6. buscar_por_cedula inexistente", lista.buscar_por_cedula("0000000000"), None)
comprobar("9. filtrar Ejecutiva", [p.nombre for p in lista.filtrar_por_clase("Ejecutiva")], ["Ana", "Diana"])
comprobar("9. filtrar Económica", [p.nombre for p in lista.filtrar_por_clase("Económica")], ["Luis", "Beto"])

comprobar("7. modificar 1003", lista.modificar(1003, "Luis M.", 42, "11A"), True)
comprobar("7. nodo no se movió", [p.nombre for p in lista.listar()], ["Ana", "Diana", "Luis M.", "Beto"])
comprobar("7. asiento nuevo", lista.buscar(1003).asiento, "11A")
comprobar("7. modificar inexistente", lista.modificar(9999, "X", 1, "1A"), False)

comprobar("8. eliminar cabeza (caso B)", lista.eliminar(1001).nombre, "Ana")
comprobar("   nueva cabeza", lista.head.data.nombre, "Diana")
comprobar("8. eliminar en medio (caso C)", lista.eliminar(1003).nombre, "Luis M.")
comprobar("   quedan", [p.nombre for p in lista.listar()], ["Diana", "Beto"])
comprobar("8. eliminar el último (caso C)", lista.eliminar(1004).nombre, "Beto")
comprobar("8. eliminar inexistente (caso D)", lista.eliminar(9999), None)
comprobar("   cantidad", lista.longitud(), 1)
comprobar("8. eliminar la única", lista.eliminar(1002).nombre, "Diana")
comprobar("   queda vacía", (lista.esta_vacia(), lista.longitud()), (True, 0))
