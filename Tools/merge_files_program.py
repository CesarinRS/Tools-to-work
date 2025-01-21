import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog

# Oculta la ventana principal de Tkinter
root = tk.Tk()
root.withdraw()

# Ventana emergente para seleccionar los archivos PDF
pdf_paths = filedialog.askopenfilenames(
    title="Selecciona los archivos PDF a unir",
    filetypes=[("Archivos PDF", "*.pdf")]
)

if not pdf_paths:
    print("No seleccionaste ningún archivo. El proceso ha terminado.")
    exit()

# Ventana emergente para guardar el archivo con nombre personalizado
output_filename = filedialog.asksaveasfilename(
    initialdir=os.path.join(os.path.expanduser("~"), "Downloads"),
    title="Guardar PDF combinado como",
    defaultextension=".pdf",
    filetypes=[("Archivos PDF", "*.pdf")]
)

if not output_filename:
    print("No seleccionaste un nombre para el archivo. El proceso ha terminado.")
    exit()

# Crear un PdfWriter para combinar las páginas
pdf_writer = PyPDF2.PdfWriter()

# Agregar las páginas de los PDFs seleccionados en el orden elegido
for pdf_path in pdf_paths:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        print(f"Agregado: {os.path.basename(pdf_path)}")
    except Exception as e:
        print(f"Error al procesar '{os.path.basename(pdf_path)}': {e}")

# Guardar el PDF combinado con el nombre especificado por el usuario
with open(output_filename, "wb") as output_file:
    pdf_writer.write(output_file)

print(f"PDF combinado guardado en: {output_filename}")
print("Proceso completado.")

