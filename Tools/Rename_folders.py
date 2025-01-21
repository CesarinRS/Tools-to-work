import os

def renombrar_carpeta(nombre):
    # Divide el nombre de la carpeta en palabras
    partes = nombre.split()
    # Si el nombre tiene 3 palabras o menos, lo deja como está
    if len(partes) <= 3:
        nombre_renombrado = nombre
    else:
        # Si tiene más de 3 palabras, usa las primeras dos y la última
        nombre_renombrado = f"{partes[0]}_{partes[1]}_{partes[-1]}"
    return nombre_renombrado

def renombrar_subcarpetas(ruta_principal):
    for root, dirs, _ in os.walk(ruta_principal, topdown=False):
        for carpeta in dirs:
            ruta_actual = os.path.join(root, carpeta)
            nuevo_nombre = renombrar_carpeta(carpeta)
            nueva_ruta = os.path.join(root, nuevo_nombre)

            # Renombrar la carpeta solo si el nombre cambió
            if ruta_actual != nueva_ruta:
                os.rename(ruta_actual, nueva_ruta)
                print(f"Carpeta renombrada: {ruta_actual} -> {nueva_ruta}")

# Ruta de la carpeta principal (ajusta según tu caso)
ruta_principal = "C:\\Users\\auxmatla\\Downloads\\prueba 1"

# Ejecutar la función
renombrar_subcarpetas(ruta_principal)
