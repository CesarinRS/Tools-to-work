import os

def reemplazar_guiones_por_espacios(nombre):
    """
    Reemplaza todos los guiones en un nombre por espacios.
    """
    return nombre.replace("_", " ")


def renombrar_archivos_y_carpetas(ruta_principal):
    """
    Renombra archivos y carpetas dentro de una ruta principal:
    - Reemplaza guiones por espacios en nombres de archivos.
    - Reemplaza guiones por espacios en nombres de carpetas.
    """
    print(f"Iniciando proceso en la ruta: {ruta_principal}")

    for root, dirs, files in os.walk(ruta_principal, topdown=False):
        print(f"\nProcesando la carpeta: {root}")

        # Renombrar archivos en la carpeta actual
        for file in files:
            print(f"  Detectado archivo: {file}")
            ruta_actual = os.path.join(root, file)
            nuevo_nombre = reemplazar_guiones_por_espacios(file)
            ruta_nueva = os.path.join(root, nuevo_nombre)

            if ruta_actual != ruta_nueva:
                try:
                    os.rename(ruta_actual, ruta_nueva)
                    print(f"  Archivo renombrado: {ruta_actual} -> {ruta_nueva}")
                except Exception as e:
                    print(f"  Error renombrando archivo {ruta_actual}: {e}")

        # Renombrar carpetas en la carpeta actual
        for carpeta in dirs:
            print(f"  Detectada carpeta: {carpeta}")
            ruta_actual = os.path.join(root, carpeta)
            nuevo_nombre = reemplazar_guiones_por_espacios(carpeta)
            ruta_nueva = os.path.join(root, nuevo_nombre)

            if ruta_actual != ruta_nueva:
                try:
                    os.rename(ruta_actual, ruta_nueva)
                    print(f"  Carpeta renombrada: {ruta_actual} -> {ruta_nueva}")
                except Exception as e:
                    print(f"  Error renombrando carpeta {ruta_actual}: {e}")

# Ruta principal de la carpeta que deseas procesar
ruta_principal = r"C:\\Users\\auxmatla\\Downloads\\prueba 1"

# Ejecutar la función
renombrar_archivos_y_carpetas(ruta_principal)
