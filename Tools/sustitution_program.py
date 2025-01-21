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

    # Pedir al usuario el número de la página que desea reemplazar
    page_to_replace = simpledialog.askinteger(
        "Página a reemplazar",
        f"Selecciona el número de la página a reemplazar (1-{total_pages}):",
        minvalue=1,
        maxvalue=total_pages
    )

    if not page_to_replace:
        print("No seleccionaste ninguna página. El proceso ha terminado.")
        exit()

    page_to_replace_index = page_to_replace - 1  # Ajustar índice (0 basado)

    # Seleccionar el archivo PDF que contiene la nueva página
    replacement_pdf_path = filedialog.askopenfilename(
        title="Selecciona el archivo PDF que contiene la nueva página",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not replacement_pdf_path:
        print("No seleccionaste ningún archivo de reemplazo. El proceso ha terminado.")
        exit()

    # Leer el archivo PDF de reemplazo
    replacement_pdf_reader = PyPDF2.PdfReader(replacement_pdf_path)
    replacement_total_pages = len(replacement_pdf_reader.pages)

    # Seleccionar la página del archivo de reemplazo
    replacement_page = simpledialog.askinteger(
        "Seleccionar nueva página",
        f"Selecciona el número de la página del archivo de reemplazo (1-{replacement_total_pages}):",
        minvalue=1,
        maxvalue=replacement_total_pages
    )

    if not replacement_page:
        print("No seleccionaste ninguna página del archivo de reemplazo. El proceso ha terminado.")
        exit()

    replacement_page_index = replacement_page - 1  # Ajustar índice (0 basado)

    # Crear un PdfWriter para construir el nuevo archivo
    pdf_writer = PyPDF2.PdfWriter()

    # Añadir todas las páginas del archivo principal, reemplazando la seleccionada
    for i in range(total_pages):
        if i == page_to_replace_index:
            # Añadir la página de reemplazo
            pdf_writer.add_page(replacement_pdf_reader.pages[replacement_page_index])
            print(f"Sustituida la página {page_to_replace} del archivo principal.")
        else:
            # Añadir la página original
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
