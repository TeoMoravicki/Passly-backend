import threading

funciones = []
funcion_id_counter = 1

lock = threading.Lock()

def get_all_funciones():
    return funciones

def get_funcion(funcion_id: int):
    for funcion in funciones:
        if funcion["id"] == funcion_id:
            return funcion
    return None

def get_funciones_by_evento(evento_id: int):
    resultado = []

    for funcion in funciones:
        if funcion["evento_id"] == evento_id:
            resultado.append(funcion)
    return resultado

def create_funcion(evento_id: int, fecha: str, horario: str, capacidad_maxima: int):
    global funcion_id_counter

    if capacidad_maxima <= 0:
        return {
            "error": "La capacidad máxima debe ser mayor a 0"
        }

    new_funcion = {
        "id": funcion_id_counter,
        "evento_id": evento_id,
        "fecha": fecha,
        "horario": horario,
        "capacidad_maxima": capacidad_maxima,
        "entradas_disponibles": capacidad_maxima,
        "estado": "ACTIVA"
    }

    funciones.append(new_funcion)
    funcion_id_counter += 1
    return new_funcion

def update_entradas_disponibles(funcion_id: int, cantidad: int):
    with lock:
        funcion = get_funcion(funcion_id)

        if not funcion:
            return {
                "error": "Función no encontrada"
            }

        if cantidad <= 0:
            return {
                "error": "La cantidad debe ser mayor a 0"
            }

        if funcion["entradas_disponibles"] < cantidad:
            return {
                "error": "No hay suficientes entradas disponibles"
            }

        funcion["entradas_disponibles"] -= cantidad
        return {
            "success": True,
            "entradas_compradas": cantidad,
            "entradas_restantes": funcion["entradas_disponibles"]
        }

def update_funcion_estado(funcion_id: int, nuevo_estado: str):
    estados_validos = [
        "ACTIVA",
        "CANCELADA",
        "FINALIZADA"
    ]
    if nuevo_estado.upper() not in estados_validos:
        return {
            "error": "Estado de función no válido"
        }
    for funcion in funciones:
        if funcion["id"] == funcion_id:
            funcion["estado"] = nuevo_estado.upper()
            return funcion
    return None