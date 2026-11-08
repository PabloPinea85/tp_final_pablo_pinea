# Ejercicio 3 - Auditoría
# Cálculo de emisiones de carbono y pruebas unitarias

# Excepción personalizada para consumo negativo
class ConsumoNegativoError(ValueError):
    """
    Se lanza cuando el consumo de kWh es negativo.
    """
    pass


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """
    Calcula las emisiones de carbono a partir del consumo de energía.
    - Si el consumo es negativo, lanza ConsumoNegativoError.
    - Si el consumo es <= 100 kWh: emisiones = consumo * factor (sin recargo)
    - Si el consumo es > 100 kWh: se aplica recargo del 1.5% sobre lo excedente
    """
    if consumo_kwh < 0:
        raise ConsumoNegativoError(
            f"El consumo no puede ser negativo: {consumo_kwh} kWh"
        )

    if consumo_kwh <= 100:
        # Sin recargo
        emisiones = consumo_kwh * factor_emision
    else:
        # Base hasta 100, el excedente se cobra con recargo del 1.5%
        base = 100 * factor_emision
        excedente = (consumo_kwh - 100) * factor_emision * 1.015
        emisiones = base + excedente

    return emisiones


def obtener_metricas_consumo(registros):
    """
    Recibe una lista de registros (diccionarios) con 'consumo_kwh' y 'planta'.
    Retorna una tupla con:
    1. Total de emisiones de todas las plantas
    2. Nombre de la planta que más emisiones generó
    """
    if not registros:
        return (0.0, "")

    total_emisiones = 0.0
    emisiones_por_planta = {}

    for registro in registros:
        consumo = registro.get("consumo_kwh", 0)
        planta = registro.get("planta", "Desconocida")

        try:
            emisiones = calcular_emisiones_carbono(consumo)
        except ValueError:
            # Si hay un error, se ignora ese registro
            continue

        total_emisiones += emisiones
        emisiones_por_planta[planta] = emisiones_por_planta.get(planta, 0) + emisiones

    # Encontrar la planta con más emisiones
    planta_mayor = max(emisiones_por_planta, key=emisiones_por_planta.get)

    return (round(total_emisiones, 2), planta_mayor)


# Bloque de pruebas unitarias
import unittest

class TestCalculoEmisiones(unittest.TestCase):
    """
    Pruebas para la función calcular_emisiones_carbono.
    """

    def test_calculo_nominal_sin_exceso(self):
        """50 kWh con factor 0.4 -> 20.0"""
        resultado = calcular_emisiones_carbono(50, 0.4)
        self.assertEqual(resultado, 20.0)

    def test_calculo_con_exceso(self):
        """120 kWh con factor 0.4:
        100 * 0.4 = 40, excedente 20 * 0.4 * 1.015 = 8.12
        Total = 48.12
        """
        resultado = calcular_emisiones_carbono(120, 0.4)
        self.assertAlmostEqual(resultado, 48.12, places=2)

    def test_calculo_excedente_mayor(self):
        """200 kWh con factor 0.4:
        100 * 0.4 = 40, excedente 100 * 0.4 * 1.015 = 40.6
        Total = 80.6
        """
        resultado = calcular_emisiones_carbono(200, 0.4)
        self.assertAlmostEqual(resultado, 80.6, places=2)

    def test_consumo_negativo_lanza_error(self):
        """Debe lanzar ConsumoNegativoError si el consumo es negativo."""
        with self.assertRaises(ConsumoNegativoError):
            calcular_emisiones_carbono(-50, 0.4)

    def test_consumo_cero(self):
        """0 kWh -> 0.0"""
        resultado = calcular_emisiones_carbono(0, 0.4)
        self.assertEqual(resultado, 0.0)

    def test_factor_por_defecto(self):
        """Si no se pasa factor, usa 0.4 por defecto."""
        resultado = calcular_emisiones_carbono(50)
        self.assertEqual(resultado, 20.0)

    def test_registros_vacio(self):
        """Una lista vacía devuelve (0.0, "")"""
        total, planta = obtener_metricas_consumo([])
        self.assertEqual(total, 0.0)
        self.assertEqual(planta, "")


# Bloque de prueba para verificar que funciona
if __name__ == "__main__":
    print("=== Test de Ejercicio 3 - Auditoría ===\n", flush=True)
    # Correr las pruebas con unittest
    unittest.main(verbosity=2)
