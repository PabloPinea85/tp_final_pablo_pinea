# Ejercicio 1 - Sensores
# Sanitización y análisis estadístico de datos de sensores

def limpiar_registro_sensor(registro_raw):
    """
    Recibe un diccionario crudo con datos de un sensor y devuelve un
    nuevo diccionario normalizado: sensor_id sin espacios, temperatura
    como float, y ubicacion con un valor por defecto si estaba vacía.
    """
    # Creamos un nuevo diccionario para no modificar el original
    registro = {}

    # sensor_id: quitamos espacios al inicio y al final
    if "sensor_id" in registro_raw and registro_raw["sensor_id"]:
        registro["sensor_id"] = str(registro_raw["sensor_id"]).strip()
    else:
        registro["sensor_id"] = ""

    # temperatura: convertir a float, quitando la C / el grado / la F / espacios
    if "temperatura" in registro_raw and registro_raw["temperatura"] is not None:
        try:
            if isinstance(registro_raw["temperatura"], (int, float)):
                registro["temperatura"] = float(registro_raw["temperatura"])
            else:
                temp = str(registro_raw["temperatura"]).strip()
                temp = (
                    temp.replace("C", "")
                    .replace("F", "")
                    .replace("°", "")
                    .replace(" ", "")
                )
                registro["temperatura"] = float(temp)
        except (ValueError, TypeError):
            registro["temperatura"] = 0.0
    else:
        registro["temperatura"] = 0.0

    # ubicacion: valor por defecto si estaba vacía o no venía
    if "ubicacion" in registro_raw:
        if registro_raw["ubicacion"] is None:
            registro["ubicacion"] = "Área No Asignada"
        else:
            ubicacion = str(registro_raw["ubicacion"]).strip()
            registro["ubicacion"] = ubicacion if ubicacion else "Área No Asignada"
    else:
        registro["ubicacion"] = "Área No Asignada"

    return registro


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Recibe la lista (ya limpia) y un umbral de temperatura.
    Devuelve una tupla: (IDs de los sensores que pasaron el umbral,
    promedio de temperatura de todos, redondeado a 2 decimales).
    Si la lista está vacía, devuelve ([], 0.0).
    """
    # Evitamos división por cero
    if not lista_sensores_limpios:
        return ([], 0.0)

    # IDs de los sensores que superan el umbral
    sensores_alerta = []
    for sensor in lista_sensores_limpios:
        if sensor.get("temperatura", 0) > umbral_temperatura:
            sensores_alerta.append(sensor.get("sensor_id", ""))

    # Promedio de temperatura
    total = 0
    cantidad = 0
    for sensor in lista_sensores_limpios:
        total += sensor.get("temperatura", 0)
        cantidad += 1

    promedio = total / cantidad
    promedio = round(promedio, 2)

    return (sensores_alerta, promedio)


# Bloque de prueba: demuestra el flujo completo
if __name__ == "__main__":
    # Lecturas crudas que llegarían de un sensor real
    lecturas_crudas = [
        {"sensor_id": "  SENSOR-001  ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "36.8°", "ubicacion": ""},
        {"sensor_id": " SENSOR-003 ", "temperatura": "18.2C", "ubicacion": "  Planta 3"},
        {"sensor_id": "SENSOR-004", "temperatura": "invalido", "ubicacion": None},
        {"sensor_id": "SENSOR-005", "temperatura": "45.0C", "ubicacion": "  Lab B"},
    ]

    print("=== Datos crudos ===")
    for lectura in lecturas_crudas:
        print(lectura)

    # Limpiamos
    print("\n=== Datos limpios ===")
    limpios = [limpiar_registro_sensor(lectura) for lectura in lecturas_crudas]
    for reg in limpios:
        print(reg)

    # Resumen con umbral de 30 grados
    umbral = 30
    alerta, promedio = generar_resumen_sensores(limpios, umbral)

    print(f"\n=== Resumen (umbral {umbral}°) ===")
    print("IDs en ALERTA:", alerta)
    print("PROMEDIO de temperatura:", promedio)
