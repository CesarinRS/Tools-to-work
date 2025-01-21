import os
import shutil

def renombrar_jpg(contador):
    # Renombra el archivo JPG a "Foto" seguido del contador si es necesario
    return f"Foto({contador})" if contador > 1 else "Foto"

def renombrar_pdf(nombre):
    # Divide el nombre en palabras
    partes = nombre.split()
    # Si el nombre tiene 3 palabras o menos, lo deja como está
    if len(partes) <= 3:
        nombre_renombrado = nombre
    else:
        # Si tiene más de 3 palabras, usa las primeras dos y la última
        nombre_renombrado = f"{partes[0]}_{partes[1]}_{partes[-1]}"
    return nombre_renombrado

def procesar_archivos(origen, destino):
    # Contador para archivos JPG
    contador_jpg = 1

    for root, _, files in os.walk(origen):
        # Obtener la ruta relativa de la carpeta actual respecto a la raíz
        ruta_relativa = os.path.relpath(root, origen)

        # Crear la estructura de carpetas en el destino sin renombrar
        carpeta_destino = os.path.join(destino, ruta_relativa)
        os.makedirs(carpeta_destino, exist_ok=True)

        for file in files:
            ruta_original = os.path.join(root, file)
            nombre_sin_ext, extension = os.path.splitext(file)

            # Renombrar y copiar archivos JPG
            if file.lower().endswith(('.jpg', '.jpeg')):
                nuevo_nombre = renombrar_jpg(contador_jpg) + extension
                ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
                contador_jpg += 1

            # Renombrar y copiar archivos PDF
            elif file.lower().endswith('.pdf'):
                nuevo_nombre = renombrar_pdf(nombre_sin_ext) + extension
                ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)

            else:
                # Si el archivo no es JPG o PDF, mantener su nombre original
                ruta_destino = os.path.join(carpeta_destino, file)

            # Copia el archivo a la ruta de destino con el nombre modificado o sin modificar según corresponda
            shutil.copy2(ruta_original, ruta_destino)
            print(f"Archivo copiado: {ruta_destino}")

# Rutas de origen y destino (ajusta las rutas según necesites)
ruta_origen = "C:\\Users\\auxmatla\\Downloads\\Requerimiento Septiembre\\completo"
ruta_destino = "C:\\Users\\auxmatla\\Downloads\\prueba 1"

# Ejecuta la función
procesar_archivos(ruta_origen, ruta_destino)
