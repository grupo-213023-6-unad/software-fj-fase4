# Software FJ — Sistema de Gestión de Clientes, Servicios y Reservas

Trabajo para el curso **Programación (213023)** de la UNAD, Fase 4
(componente práctico).

## De qué se trata

Es un sistema orientado a objetos para manejar clientes, servicios
(reserva de salas, alquiler de equipos y asesorías especializadas) y
reservas de una empresa ficticia llamada Software FJ. No usa base de
datos, todo vive en listas en memoria mientras corre el programa.

Cosas que se aplicaron:

- Clases abstractas (`EntidadBase` y `Servicio`)
- Herencia (`Cliente`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`)
- Polimorfismo: cada servicio calcula su costo y se describe distinto
- Encapsulación con `@property` y validación en cada setter
- Excepciones propias, `try/except/else/finally` y encadenamiento con `raise ... from ...`
- Logging a archivo en vez de solo prints (`logs/software_fj.log`)

## Estructura

```
software_fj/
├── excepciones.py     # Excepciones propias del sistema
├── logger_config.py   # Configuración del logging a archivo
├── entidades.py        # EntidadBase, Cliente, Servicio y sus 3 subclases
├── reserva.py          # Clase Reserva (estado, confirmación, cancelación, pago)
├── gestor.py            # GestorFJ: orquesta clientes, servicios y reservas
├── main.py              # 19 operaciones de prueba (válidas e inválidas)
└── logs/
    └── software_fj.log  # se genera solo al ejecutar
```

## Cómo correrlo

Necesita Python 3.10+, nada de librerías externas.

```bash
python main.py
```

Al terminar, mira `logs/software_fj.log` para ver el detalle de todo
lo que pasó durante la ejecución.

## Qué hace `main.py`

| # | Operación | Resultado esperado |
|---|-----------|---------------------|
| 1-2 | Registrar clientes válidos | Éxito |
| 3-4 | Registrar clientes inválidos (correo/nombre) | Error controlado |
| 5-7 | Crear los 3 tipos de servicio | Éxito |
| 8-9 | Crear servicios inválidos (costo negativo / dato faltante) | Error controlado |
| 10-12 | Crear reservas válidas (con y sin parámetros extra) | Éxito |
| 13-15 | Crear reservas inválidas (duración 0, servicio no disponible, descuento fuera de rango) | Error controlado |
| 16-17 | Cancelar una reserva y luego intentar cancelarla de nuevo | Éxito / Error controlado |
| 18 | Procesar pago de una reserva confirmada | Éxito |
| 19 | Procesar pago de una reserva cancelada | Error controlado |

El programa no se detiene en ningún punto: todos los errores se
capturan, quedan en el log, y sigue corriendo hasta imprimir el
resumen final.
## Repositorio

Enlace del repositorio: https://github.com/grupo-213023-6-unad/software-fj-fase4

## Colaboradores

- Jefferson David (implementación y documentación del sistema)

## Conclusiones técnicas

El desarrollo de este sistema permitió aplicar los principios de programación
orientada a objetos (abstracción, herencia, polimorfismo y encapsulación) en un
caso de uso realista. El manejo estructurado de excepciones garantizó que el
programa se mantuviera estable incluso ante datos inválidos o operaciones no
permitidas, y el registro en archivo de logs facilitó el seguimiento de errores
sin exponer información técnica al usuario final.

## Autoría

Trabajo colaborativo — Curso Programación 213023, UNAD.

