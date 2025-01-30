"""
This scripts rotate PDF files pages 
"""

import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

# Hide the main tkinter window
# Oculta la ventana principal de Tkinter
root = tk.Tk()
root.withdraw()

# Select PDF files window 
# Ventana emergente para seleccionar los archivos PDF
pdf_paths = filedialog.askopenfilenames(
    title="Selecciona los archivos PDF a rotar",
    filetypes=[("Archivos PDF", "*.pdf")]
)

if not pdf_paths:
    print("No seleccionaste ningún archivo. El proceso ha terminado.")
    exit()

# PFD files process separated
# Procesar cada archivo PDF por separado
for pdf_path in pdf_paths:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)

        # Request user page for rotate
        # Pedir al usuario las páginas que desea rotar
        pages_to_rotate = simpledialog.askstring(
            "Seleccionar páginas",
            f"Ingrese los números de las páginas a rotar para '{os.path.basename(pdf_path)}' (separados por comas, rango con '-'; ej: 1,3-5):\n(Total de páginas: {total_pages})"
        )

        if not pages_to_rotate:
            print(f"No se rotaron páginas del archivo '{os.path.basename(pdf_path)}'.")
            continue

        # Transform page numbers enter to lists
        # Convertir las entradas a una lista de números de páginas
        pages_to_rotate = pages_to_rotate.replace(" ", "").split(",")
        selected_pages = []
        for item in pages_to_rotate:
            if "-" in item:
                start, end = map(int, item.split("-"))
                selected_pages.extend(range(start, end + 1))
            else:
                selected_pages.append(int(item))
        pages_to_rotate = [p - 1 for p in selected_pages if 1 <= p <= total_pages]

        # Request rotate grade
        # Preguntar el grado de rotación
        rotation_angle = simpledialog.askinteger(
            "Rotación de PDFs",
            "Especifica los grados de rotación (90, 180, 270):",
            minvalue=90,
            maxvalue=270
        )

        if rotation_angle not in [90, 180, 270]:
            print(f"Ángulo de rotación inválido para '{os.path.basename(pdf_path)}'.")
            continue
#

        # Create PdfWriter to save files
        # Crear un PdfWriter para guardar el archivo actual
        pdf_writer = PyPDF2.PdfWriter()

        # Select pages rotates
        # Rotar las páginas seleccionadas
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            if page_num in pages_to_rotate:
                page.rotate(rotation_angle)
                print(f"Page {page_num + 1} rotate become '{os.path.basename(pdf_path)}'.")
            pdf_writer.add_page(page)

        # Save as custom name PDF file rotated
        # Guardar el archivo rotado con un nombre personalizado
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_filename = filedialog.asksaveasfilename(
            initialfile=f"{base_name}_rotate.pdf",
            title=f"Guardar archivo rotado de '{base_name}' as:",
            defaultextension=".pdf",
            filetypes=[("PDF file", "*.pdf")]
        )
# "PDF file rotated saved"


        if not output_filename:
            print(f"No se guardó el archivo rotado de '{base_name}'.")
            continue
# "The PDF file rotate wasn't saved"
        with open(output_filename, "wb") as output_file:
            pdf_writer.write(output_file)

        print(f"Archivo rotado guardado: {output_filename}")
# "Rotate file save as: "
    except Exception as e:
        print(f"Error al procesar '{os.path.basename(pdf_path)}': {e}")
# "Error processing"
print("Proceso completado.")
# "Process has been terminated"
