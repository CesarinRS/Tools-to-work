import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

def girar_paginas_pares(pdf_entrada, pdf_salida):
    # Cargar el PDF de entrada
    lector = PdfReader(pdf_entrada)
    escritor = PdfWriter()

    # Recorrer todas las páginas del PDF
    for i, pagina in enumerate(lector.pages):
        if (i + 1) % 2 == 0:  # Verifica si es una página par
            pagina.rotate(90)  # Gira la página 90° hacia la derecha
        escritor.add_page(pagina)

    # Guardar el nuevo PDF
    with open(pdf_salida, "wb") as archivo_salida:
        escritor.write(archivo_salida)

def seleccionar_archivo():
    archivo_entrada = filedialog.askopenfilename(
        title="Selecciona un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if not archivo_entrada:
        messagebox.showerror("Error", "No seleccionaste ningún archivo.")
        return

    archivo_salida = filedialog.asksaveasfilename(
        title="Guardar como",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if not archivo_salida:
        messagebox.showerror("Error", "No seleccionaste un destino para guardar el archivo.")
        return

    try:
        girar_paginas_pares(archivo_entrada, archivo_salida)
        messagebox.showinfo("Éxito", f"Archivo guardado exitosamente en:\n{archivo_salida}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Girar Páginas Pares de un PDF")
ventana.geometry("400x200")

etiqueta = tk.Label(ventana, text="Presiona el botón para seleccionar un archivo PDF")
etiqueta.pack(pady=20)

boton = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
boton.pack(pady=10)

ventana.mainloop()

