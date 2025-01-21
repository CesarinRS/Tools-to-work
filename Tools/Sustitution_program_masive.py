import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog

# Oculta la ventana principal de Tkinter
root = tk.Tk()
root.withdraw()

# Pedir al usuario que seleccione la carpeta con los archivos PDF
folder_path = filedialog.askdirectory(
    title="Selecciona la carpeta con los archivos PDF a procesar"
)

if not folder_path:
    print("No seleccionaste ninguna carpeta. El proceso ha terminado.")
    exit()

# Listar todos los PDFs en la carpeta seleccionada
pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]

if not pdf_files:
    print("No se encontraron archivos PDF en la carpeta seleccionada.")
    exit()

# Pedir al usuario el número de la hoja a sustituir
page_to_replace = int(input("Introduce el número de la hoja a sustituir (empezando en 1): ")) - 1

# Pedir el archivo PDF con la hoja nueva
new_page_path = filedialog.askopenfilename(
    title="Selecciona el archivo PDF con la nueva hoja",
    filetypes=[("Archivos PDF", "*.pdf")]
)

if not new_page_path:
    print("No seleccionaste un archivo para la nueva hoja. El proceso ha terminado.")
    exit()

# Leer la nueva hoja desde el archivo seleccionado
with open(new_page_path, "rb") as new_pdf_file:
    new_pdf_reader = PyPDF2.PdfReader(new_pdf_file)
    new_page = new_pdf_reader.pages[0]  # Asume que solo contiene una página

# Procesar cada archivo PDF en la carpeta
for pdf_path in pdf_files:
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            # Sustituir la página en la posición indicada
            for i, page in enumerate(pdf_reader.pages):
                if i == page_to_replace:
                    pdf_writer.add_page(new_page)
                    print(f"Página {page_to_replace + 1} sustituida en '{os.path.basename(pdf_path)}'.")
                else:
                    pdf_writer.add_page(page)

            # Guardar el archivo modificado
            output_path = os.path.join(folder_path, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_modificado.pdf")
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

        print(f"Archivo procesado y guardado: {output_path}")

    except Exception as e:
        print(f"Error al procesar '{pdf_path}': {e}")

print("Proceso completado.")

