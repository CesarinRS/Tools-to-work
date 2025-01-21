import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

def select_pdf1():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf1.delete(0, tk.END)
        entry_pdf1.insert(0, file_path)

def select_pdf2():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf2.delete(0, tk.END)
        entry_pdf2.insert(0, file_path)

def merge_pdfs():
    pdf1_path = entry_pdf1.get()
    pdf2_path = entry_pdf2.get()
    try:
        insert_position = int(entry_position.get())
    except ValueError:
        messagebox.showerror("Error", "La posición debe ser un número entero válido.")
        return

    if not pdf1_path or not pdf2_path:
        messagebox.showerror("Error", "Debe seleccionar ambos archivos PDF.")
        return

    try:
        # Leer ambos PDFs
        pdf1_reader = PdfReader(pdf1_path)
        pdf2_reader = PdfReader(pdf2_path)
        pdf_writer = PdfWriter()

        # Validar posición
        if insert_position < 1 or insert_position > len(pdf1_reader.pages):
            messagebox.showerror("Error", "La posición está fuera del rango válido.")
            return

        # Agregar páginas del PDF1 hasta la posición
        for i in range(insert_position - 1):
            pdf_writer.add_page(pdf1_reader.pages[i])

        # Agregar todas las páginas del PDF2
        for page in pdf2_reader.pages:
            pdf_writer.add_page(page)

        # Agregar el resto de las páginas del PDF1
        for i in range(insert_position - 1, len(pdf1_reader.pages)):
            pdf_writer.add_page(pdf1_reader.pages[i])

        # Guardar el PDF combinado
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)
            messagebox.showinfo("Éxito", "Los PDFs se han combinado correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al combinar los PDFs: {e}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Insertar PDF dentro de otro PDF")

# Widgets para el PDF1
label_pdf1 = tk.Label(root, text="Seleccionar PDF1:")
label_pdf1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_pdf1 = tk.Entry(root, width=50)
entry_pdf1.grid(row=0, column=1, padx=10, pady=5)
button_pdf1 = tk.Button(root, text="Examinar", command=select_pdf1)
button_pdf1.grid(row=0, column=2, padx=10, pady=5)

# Widgets para el PDF2
label_pdf2 = tk.Label(root, text="Seleccionar PDF2:")
label_pdf2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_pdf2 = tk.Entry(root, width=50)
entry_pdf2.grid(row=1, column=1, padx=10, pady=5)
button_pdf2 = tk.Button(root, text="Examinar", command=select_pdf2)
button_pdf2.grid(row=1, column=2, padx=10, pady=5)

# Widgets para la posición
label_position = tk.Label(root, text="Posición de inserción (Insertar despues del numero de pag ingresado):")
label_position.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_position = tk.Entry(root, width=10)
entry_position.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Botón para combinar PDFs
button_merge = tk.Button(root, text="Combinar PDFs", command=merge_pdfs)
button_merge.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()