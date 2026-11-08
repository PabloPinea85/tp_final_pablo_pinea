# Ejercicio 2 - Productos
# Modelo de productos, excepciones y persistencia

# Excepción personalizada para stock inválido
class StockInvalidoError(Exception):
    """
    Se lanza cuando se intenta asignar un stock negativo.
    """
    def __init__(self, mensaje="El stock no puede ser un valor negativo."):
        super().__init__(mensaje)


# Clase base para dispositivos ecológicos
class DispositivoEcologico:
    """
    Clase base que centraliza el estado común de los productos
    sustentables y encapsula el stock (no puede ser negativo).
    """
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        # Variable de respaldo privada para el stock
        self._stock = 0
        # Invocamos el setter para validar el stock desde el inicio
        self.stock = stock

    @property
    def stock(self):
        """Retorna el valor actual del stock."""
        return self._stock

    @stock.setter
    def stock(self, valor):
        """
        Valida que el stock no sea negativo.
        Si es negativo, lanza StockInvalidoError.
        """
        if valor < 0:
            raise StockInvalidoError(
                f"El stock del producto {self.nombre} no puede ser negativo: {valor}"
            )
        self._stock = valor

    def generar_ficha_tecnica(self):
        """
        Retorna la ficha técnica básica del producto.
        El precio se formatea como un string monetario con dos decimales.
        """
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": f"${self.precio:.2f}",
            "stock": self._stock
        }


# Subclase especializada: PanelSolar
class PanelSolar(DispositivoEcologico):
    """
    Representa un panel solar. Hereda de DispositivoEcologico
    y añade los atributos de ingeniería: eficiencia y potencia.
    """
    def __init__(self, id_producto, nombre, precio, stock, eficiencia, potencia_w):
        super().__init__(id_producto, nombre, precio, stock)
        self.eficiencia = eficiencia
        self.potencia_w = potencia_w

    def generar_ficha_tecnica(self):
        """
        Sobrescritura del método de la clase base.
        Aplica polimorfismo: añade los datos específicos del panel.
        """
        # Diccionario base de la clase madre
        ficha = super().generar_ficha_tecnica()
        # Añadimos los datos propios del panel
        ficha.update({
            "tipo": "Panel Solar",
            "potencia_w": self.potencia_w,
            "eficiencia": self.eficiencia
        })
        return ficha


# Gestor del catálogo (persistencia en JSON)
class GestorInventario:
    """
    Gestiona la lista de dispositivos y guarda el catálogo en un archivo JSON.
    """
    def __init__(self):
        self.dispositivos = []

    def agregar_dispositivo(self, dispositivo):
        """Agrega un dispositivo a la lista."""
        self.dispositivos.append(dispositivo)

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        """
        Serializa la lista de dispositivos en un archivo JSON.
        Usa el método generar_ficha_tecnica() de cada objeto.
        """
        import json

        # Construimos una lista de diccionarios para guardar
        catalogo = []
        for dispositivo in lista_dispositivos:
            catalogo.append(dispositivo.generar_ficha_tecnica())

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, indent=4, ensure_ascii=False)

        return len(catalogo)


# Bloque de prueba
if __name__ == "__main__":
    print("=== Test de Ejercicio 2 - Productos ===\n")

    # 1. Crear un panel solar válido
    panel = PanelSolar(
        id_producto="PS-001",
        nombre="Solar Uno",
        precio=300,
        stock=10,
        eficiencia=22.5,
        potencia_w=300
    )

    print("Ficha técnica del panel:")
    print(panel.generar_ficha_tecnica())

    # 2. Intentar asignar stock negativo (debe fallar)
    print("\nIntentamos asignar stock -5 al panel...")
    try:
        panel.stock = -5
        print("ERROR: no se capturó la excepción")
    except StockInvalidoError as e:
        print(f"CAPTURAMOS EL ERROR: {e}")

    # 3. Guardar el catálogo con los productos válidos
    print("\nGuardando catálogo en catalogo_ecotech.json...")
    gestor = GestorInventario()
    gestor.agregar_dispositivo(panel)
    ruta = "catalogo_ecotech.json"
    cantidad = gestor.guardar_catalogo_json(gestor.dispositivos, ruta)
    print(f"Se guardaron {cantidad} producto(s) en {ruta}")

    # 4. Leer de vuelta para verificar
    print("\nContenido del archivo JSON:")
    import json
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = json.load(archivo)
    print(json.dumps(contenido, indent=4, ensure_ascii=False))
