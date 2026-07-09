"""
main.py

Punto de entrada. Corre 19 operaciones para probar el sistema:
registros válidos e inválidos de clientes, servicios bien y mal
creados, reservas exitosas y fallidas, etc. La idea es que sin
importar cuántos errores se simulen, el programa termine solo hasta
el final y todo quede en logs/software_fj.log.

    python main.py
"""

from entidades import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorFJ
from excepciones import SoftwareFJError


def linea(titulo: str):
    print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")


def main():
    gestor = GestorFJ()

    # --- BLOQUE 1: registro de clientes (2 válidos, 2 inválidos) ---
    linea("BLOQUE 1: Registro de clientes")

    try:
        cliente1 = Cliente("C001", "Ana Torres", "1020304050",
                            "ana.torres@correo.com", "3011234567")
        exito = gestor.registrar_cliente(cliente1)
        print(f"[1] Registro cliente válido -> {'OK' if exito else 'FALLÓ'}")
    except SoftwareFJError as e:
        print(f"[1] Error inesperado creando cliente1: {e}")

    try:
        cliente2 = Cliente("C002", "Luis Pérez", "1122334455",
                            "luis.perez@correo.com", "3157654321")
        exito = gestor.registrar_cliente(cliente2)
        print(f"[2] Registro cliente válido -> {'OK' if exito else 'FALLÓ'}")
    except SoftwareFJError as e:
        print(f"[2] Error inesperado creando cliente2: {e}")

    # correo sin arroba -> debe fallar
    try:
        cliente_malo = Cliente("C003", "Marta Ruiz", "1234567890",
                                "correo-sin-arroba.com", "3009998888")
        gestor.registrar_cliente(cliente_malo)
        print("[3] Registro cliente inválido -> OK (no debería pasar)")
    except SoftwareFJError as e:
        print(f"[3] Registro cliente inválido -> Capturado correctamente: {e}")

    # nombre con números -> debe fallar
    try:
        cliente_malo2 = Cliente("C004", "Pedro123", "9988776655",
                                 "pedro@correo.com", "3001112233")
        gestor.registrar_cliente(cliente_malo2)
        print("[4] Registro cliente inválido -> OK (no debería pasar)")
    except SoftwareFJError as e:
        print(f"[4] Registro cliente inválido -> Capturado correctamente: {e}")

    # --- BLOQUE 2: creación de servicios ---
    linea("BLOQUE 2: Creación de servicios")

    try:
        sala1 = ReservaSala("S001", "Sala Principal", 50000, capacidad=20)
        exito = gestor.registrar_servicio(sala1)
        print(f"[5] Crear ReservaSala válida -> {'OK' if exito else 'FALLÓ'}")
    except SoftwareFJError as e:
        print(f"[5] Error creando sala: {e}")

    try:
        equipo1 = AlquilerEquipo("S002", "Proyector 4K", 30000,
                                  tipo_equipo="Proyector")
        exito = gestor.registrar_servicio(equipo1)
        print(f"[6] Crear AlquilerEquipo válido -> {'OK' if exito else 'FALLÓ'}")
    except SoftwareFJError as e:
        print(f"[6] Error creando equipo: {e}")

    try:
        asesoria1 = AsesoriaEspecializada("S003", "Asesoría en Ciberseguridad",
                                           80000, area_experticia="Seguridad")
        exito = gestor.registrar_servicio(asesoria1)
        print(f"[7] Crear AsesoriaEspecializada válida -> "
              f"{'OK' if exito else 'FALLÓ'}")
    except SoftwareFJError as e:
        print(f"[7] Error creando asesoría: {e}")

    # costo_base negativo -> debe fallar
    try:
        sala_mala = ReservaSala("S004", "Sala Fantasma", -10000, capacidad=5)
        gestor.registrar_servicio(sala_mala)
        print("[8] Crear servicio con costo negativo -> OK (no debería pasar)")
    except SoftwareFJError as e:
        print(f"[8] Crear servicio con costo negativo -> Capturado: {e}")

    # sin tipo_equipo -> debe fallar
    try:
        equipo_malo = AlquilerEquipo("S005", "Equipo sin tipo", 20000,
                                      tipo_equipo="")
        gestor.registrar_servicio(equipo_malo)
        print("[9] Crear equipo sin tipo -> OK (no debería pasar)")
    except SoftwareFJError as e:
        print(f"[9] Crear equipo sin tipo -> Capturado: {e}")

    # --- BLOQUE 3: reservas ---
    linea("BLOQUE 3: Reservas")

    # sobrecarga simple, solo horas
    reserva1 = gestor.crear_reserva("R001", cliente1, sala1, duracion=3)
    print(f"[10] Reserva simple -> "
          f"{'OK, costo=' + str(reserva1.costo_final) if reserva1 else 'FALLÓ'}")

    # con impuesto y descuento
    reserva2 = gestor.crear_reserva("R002", cliente2, sala1, duracion=2,
                                     impuesto=0.19, descuento=0.10)
    print(f"[11] Reserva con impuesto y descuento -> "
          f"{'OK, costo=' + str(reserva2.costo_final) if reserva2 else 'FALLÓ'}")

    # alquiler de equipo
    reserva3 = gestor.crear_reserva("R003", cliente1, equipo1, duracion=4,
                                     impuesto=0.19)
    print(f"[12] Reserva de equipo -> "
          f"{'OK, costo=' + str(reserva3.costo_final) if reserva3 else 'FALLÓ'}")

    # duración 0 -> debe fallar
    reserva4 = gestor.crear_reserva("R004", cliente2, asesoria1, duracion=0)
    print(f"[13] Reserva con duración 0 -> "
          f"{'OK (no debería pasar)' if reserva4 else 'FALLÓ correctamente'}")

    # servicio no disponible -> debe fallar
    equipo1.disponible = False
    reserva5 = gestor.crear_reserva("R005", cliente1, equipo1, duracion=2)
    print(f"[14] Reserva a servicio no disponible -> "
          f"{'OK (no debería pasar)' if reserva5 else 'FALLÓ correctamente'}")
    equipo1.disponible = True  # lo dejamos disponible otra vez

    # descuento fuera de rango -> debe fallar
    reserva6 = gestor.crear_reserva("R006", cliente2, sala1, duracion=1,
                                     descuento=1.5)
    print(f"[15] Reserva con descuento inválido (150%) -> "
          f"{'OK (no debería pasar)' if reserva6 else 'FALLÓ correctamente'}")

    # --- BLOQUE 4: confirmación / cancelación / pago ---
    linea("BLOQUE 4: Ciclo de vida de reservas")

    exito_cancelar = gestor.cancelar_reserva("R001", "El cliente cambió de fecha")
    print(f"[16] Cancelar reserva confirmada -> "
          f"{'OK' if exito_cancelar else 'FALLÓ'}")

    # cancelar la misma reserva otra vez -> debe fallar
    exito_cancelar_dup = gestor.cancelar_reserva("R001", "Doble cancelación")
    print(f"[17] Cancelar reserva ya cancelada -> "
          f"{'OK (no debería pasar)' if exito_cancelar_dup else 'FALLÓ correctamente'}")

    if reserva2:
        try:
            resultado_pago = reserva2.procesar_pago()
            print(f"[18] Procesar pago -> OK: {resultado_pago}")
        except SoftwareFJError as e:
            print(f"[18] Procesar pago -> Error controlado: {e}")

    # cancelamos reserva3 antes para forzar el error de pago
    if reserva3:
        gestor.cancelar_reserva("R003", "Prueba de error de pago")
        try:
            reserva3.procesar_pago()
            print("[19] Procesar pago de reserva cancelada -> OK (no debería pasar)")
        except SoftwareFJError as e:
            print(f"[19] Procesar pago de reserva cancelada -> "
                  f"Capturado correctamente: {e}")

    # --- RESUMEN FINAL ---
    linea("RESUMEN FINAL")
    print(f"Clientes registrados: {len(gestor.listar_clientes())}")
    print(f"Servicios registrados: {len(gestor.listar_servicios())}")
    print(f"Reservas creadas: {len(gestor.listar_reservas())}")
    print("\nRevisa el archivo 'logs/software_fj.log' para ver el registro "
          "detallado de todos los eventos y errores.")
    print("\nEl programa terminó sin interrupciones, a pesar de los "
          "errores simulados.")


if __name__ == "__main__":
    main()
