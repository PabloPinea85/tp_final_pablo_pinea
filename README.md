# Trabajo Final - FESAT 2026

Trabajo práctico final de Pablo Pinea.

Son tres ejercicios de Python y una página web.

## Qué hay en cada carpeta

**ejercicio_1_sensores/**

Toma los datos que mandan los sensores, que vienen desprolijos (con espacios de más,
con la letra C pegada, con cosas que no son números), y los deja ordenados.
Después saca el promedio de temperatura y dice qué sensores pasaron el límite.

**ejercicio_2_productos/**

Arma los productos de la empresa. El stock nunca puede quedar en negativo: si alguien
intenta poner un número negativo, el programa avisa con un error en vez de romperse.
Al final guarda todo en un archivo llamado `catalogo_ecotech.json`.

**ejercicio_3_auditoria_web/**

Calcula cuánto contamina cada planta según la energía que consume. Tiene 7 pruebas
automáticas que revisan que las cuentas estén bien.

**proyecto_django_temp/**

La página web. Muestra una tabla con el consumo de cada planta y el total de emisiones.

## Cómo probarlo

Hace falta tener Python instalado.

1. Instalar lo que necesita el proyecto:

   ```
   pip install -r requirements.txt
   ```

2. Correr los tres ejercicios (parado en la carpeta principal). Cada uno muestra
   su resultado en la pantalla:

   ```
   python ejercicio_1_sensores/sensores.py
   python ejercicio_2_productos/inventario.py
   python ejercicio_3_auditoria_web/emisiones.py
   ```

3. Abrir la página web:

   ```
   cd proyecto_django_temp
   python manage.py runserver
   ```

   Y en el navegador entrar a: http://127.0.0.1:8000/sustentabilidad/

## Pruebas automáticas

El ejercicio 3 y la página web ya vienen con pruebas que se corren solas:

- Ejercicio 3: se corren al ejecutar `emisiones.py` (son las 7 del punto anterior).
- Página web: `cd proyecto_django_temp` y después `python manage.py test`.
