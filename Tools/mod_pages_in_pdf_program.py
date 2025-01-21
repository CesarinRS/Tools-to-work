import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

# Oculta la ventana principal de Tkinter
root = tk.Tk()
root.withdraw()

# Seleccionar el archivo PDF principal
main_pdf_path = filedialog.askopenfilename(
    title="Selecciona el archivo PDF principal",
    filetypes=[("Archivos PDF", "*.pdf")]
)

if not main_pdf_path:
    print("No seleccionaste ningún archivo. El proceso ha terminado.")
    exit()

try:
    # Leer el archivo PDF principal
    pdf_reader = PyPDF2.PdfReader(main_pdf_path)
    total_pages = len(pdf_reader.pages)

    # Pedir al usuario el número de la página que desea mover
    page_to_move = simpledialog.askinteger(
        "Página a mover",
        f"Selecciona el número de la página a mover (1-{total_pages}):",
        minvalue=1,
        maxvalue=total_pages
    )

    if not page_to_move:
        print("No seleccionaste ninguna página. El proceso ha terminado.")
        exit()

    page_to_move_index = page_to_move - 1  # Ajustar índice (0 basado)

    # Crear un PdfWriter para construir el nuevo archivo
    pdf_writer = PyPDF2.PdfWriter()

    # Primero, agregar la página seleccionada al principio
    pdf_writer.add_page(pdf_reader.pages[page_to_move_index])
    print(f"Página {page_to_move} movida al principio.")

    # Luego, agregar todas las demás páginas (excepto la seleccionada) en su orden original
    for i in range(total_pages):
        if i != page_to_move_index:
            pdf_writer.add_page(pdf_reader.pages[i])

    # Guardar el archivo modificado con un nombre personalizado
    base_name = os.path.splitext(os.path.basename(main_pdf_path))[0]
    output_filename = filedialog.asksaveasfilename(
        initialfile=f"{base_name}_modificado.pdf",
        title="Guardar archivo modificado como",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not output_filename:
        print("No se guardó el archivo modificado.")
        exit()

    with open(output_filename, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"Archivo modificado guardado: {output_filename}")

except Exception as e:
    print(f"Error al procesar los archivos: {e}")

print("Proceso completado.")
