import os
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk
from tkinter.filedialog import askdirectory

def voltear_pdfs(carpeta_origen, carpeta_destino):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    for archivo in os.listdir(carpeta_origen):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta_origen, archivo)
            reader = PdfReader(ruta_pdf)
            total_paginas = len(reader.pages)

            # Verificar si el archivo tiene exactamente 2 páginas
            if total_paginas == 2:
                writer = PdfWriter()
                # Agregar la página 2 primero y luego la página 1
                writer.add_page(reader.pages[1])
                writer.add_page(reader.pages[0])

                # Guardar el archivo con sufijo "_volteo"
                nuevo_nombre = f"{os.path.splitext(archivo)[0]}_volteo.pdf"
                ruta_nueva = os.path.join(carpeta_destino, nuevo_nombre)
                with open(ruta_nueva, "wb") as nuevo_pdf:
                    writer.write(nuevo_pdf)
                print(f"Archivo procesado: {archivo}")
            else:
                print(f"Archivo ignorado (no tiene exactamente 2 páginas): {archivo}")

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

    print("Selecciona la carpeta de destino donde se guardarán los PDFs volteados:")
    carpeta_destino = askdirectory(title="Selecciona la carpeta de destino")
    if not carpeta_destino:
        print("No seleccionaste una carpeta de destino. Saliendo...")
        exit()

    # Ejecutar la función
    voltear_pdfs(carpeta_origen, carpeta_destino)
