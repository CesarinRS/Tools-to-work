"""
This script has been created because im needed change very much names in sub-folders in main folder
"""

import os
import shutil

def rename_jpg(accountant):
    # JPG file has been renamed of "Picture" with accounting between only if necesary  
    # Renombra el archivo JPG a "Foto" seguido del contador si es necesario
    return f"Picture({accountant})" if accountant > 1 else "Picture"

def rename_pdf(name):
    # Divide el nombre en palabras
    parts = name.split()
    # Si el nombre tiene 3 palabras o menos, lo deja como está
    
    if len(parts) <= 3:
        name_renamed = name
    else:
        # If have more 3 words apply then name first, second and last
        # Si tiene más de 3 palabras, usa las primeras dos y la última
        name_renamed = f"{parts[0]}_{parts[1]}_{parts[-1]}"
    return name_renamed

def files_processor(origin, destiny):
    # Accountant for JPG files
    # Contador para archivos JPG
    accountant_jpg = 1

    for root, _, files in os.walk(origin):
        # Obtener la ruta relativa de la carpeta actual respecto a la raíz
        # Regarding of the root, get the relative rute of folder selected 
        relative_rute = os.path.relpath(root, origin)

        # Crear la estructura de carpetas en el destino sin renombrar
        # Structure destiny folder are create hasn't rename
        destiny_folder = os.path.join(destiny, relative_rute)
        os.makedirs(destiny_folder, exist_ok=True)

        for file in files:
            origin_rute = os.path.join(root, file)
            name_without_ext, extension = os.path.splitext(file)

            # Renombrar y copiar archivos JPG
            # JPG files are renamed and copy
            if file.lower().endswith(('.jpg', '.jpeg')):
                new_name = rename_jpg(accountant_jpg) + extension
                destiny_rute = os.path.join(destiny_folder, new_name)
                accountant_jpg += 1

            # Renombrar y copiar archivos PDF
            # PDF files are renamed and copy
            elif file.lower().endswith('.pdf'):
                nuevo_nombre = rename_pdf(name_without_ext) + extension
                destiny_rute = os.path.join(destiny_folder, nuevo_nombre)

            else:
                # Si el archivo no es JPG o PDF, mantener su nombre original
                # Name stay the same if file isn't JPG or PDF
                destiny_rute = os.path.join(destiny_folder, file)

            # Copia el archivo a la ruta de destino con el nombre modificado o sin modificar según corresponda
            # Copy the file and sent on the destiny rute, with the modified name or same
            shutil.copy2(origin_rute, destiny_rute)
            print(f"copied file: {destiny_rute}")

# Rutas de origen y destino
# Origin and destiny rutes
origin_rute = os.path.join()
destiny_rute = os.path.join()

# Function execute
files_processor(origin_rute, destiny_rute)
