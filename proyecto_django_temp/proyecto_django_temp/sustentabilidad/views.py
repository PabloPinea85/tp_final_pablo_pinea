from django.shortcuts import render

# Importamos la función que procesa las métricas del ejercicio 3
from ejercicio_3_auditoria_web.emisiones import obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    """
    Vista que muestra el panel de auditoría de sostenibilidad.
    Procesa las métricas de consumo y renderiza la plantilla HTML.
    """
    # Datos simulados: historial de consumo por planta
    registros = [
        {"planta": "Planta Norte", "consumo_kwh": 150},
        {"planta": "Planta Sur", "consumo_kwh": 90},
        {"planta": "Planta Este", "consumo_kwh": 200},
        {"planta": "Planta Oeste", "consumo_kwh": 75},
    ]

    # Procesamos las métricas
    total_emisiones, planta_mayor = obtener_metricas_consumo(registros)

    # Preparamos el diccionario de contexto para la plantilla
    contexto = {
        "registros": registros,
        "total_emisiones": total_emisiones,
        "planta_mayor": planta_mayor,
    }

    return render(request, "sustentabilidad/panel.html", contexto)
