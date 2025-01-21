import os
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk
from tkinter.filedialog import askdirectory

def dividir_pdfs(carpeta_origen, carpeta_destino):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    for archivo in os.listdir(carpeta_origen):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta_origen, archivo)
            reader = PdfReader(ruta_pdf)
            total_paginas = len(reader.pages)

            # Verificar si cumple las condiciones
            if total_paginas > 2 and total_paginas % 2 == 0:
                for i in range(0, total_paginas, 2):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])      # Agregar la primera hoja del par
                    writer.add_page(reader.pages[i + 1])  # Agregar la segunda hoja del par

                    # Crear un nuevo archivo para cada par de hojas
                    nuevo_nombre = f"{os.path.splitext(archivo)[0]}_mod_{i//2 + 1}.pdf"
                    ruta_nueva = os.path.join(carpeta_destino, nuevo_nombre)
                    with open(ruta_nueva, "wb") as nuevo_pdf:
                        writer.write(nuevo_pdf)
                print(f"Archivo procesado: {archivo}")
            else:
                print(f"Archivo ignorado (no cumple condiciones): {archivo}")

# Configuración con ventanas emergentes
if __name__ == "__main__":
    # Ocultar ventana principal de Tkinter
    Tk().withdraw()

    # Preguntar al usuario por las carpetas
    print("Selecciona la carpeta de origen donde están los PDFs:")
    carpeta_origen = askdirectory(title="Selecciona la carpeta de origen")
    if not carpeta_origen:
        print("No seleccionaste una carpeta de origen. Saliendo...")
        exit()

    print("Selecciona la carpeta de destino donde se guardarán los PDFs:")
    carpeta_destino = askdirectory(title="Selecciona la carpeta de destino")
    if not carpeta_destino:
        print("No seleccionaste una carpeta de destino. Saliendo...")
        exit()

    # Ejecutar la función
    dividir_pdfs(carpeta_origen, carpeta_destino)
