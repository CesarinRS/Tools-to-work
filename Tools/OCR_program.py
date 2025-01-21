import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Ruta a Tesseract

def select_pdf():
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if file_path:
        load_pdf(file_path)

def load_pdf(file_path):
    global pdf_doc, pdf_page, canvas, tk_image, page_image
    pdf_doc = fitz.open(file_path)
    pdf_page = pdf_doc[0]  # Carga la primera página

    # Renderiza la página como una imagen
    pix = pdf_page.get_pixmap()
    page_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    tk_image = ImageTk.PhotoImage(page_image)

    # Muestra la imagen en el canvas
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.config(scrollregion=canvas.bbox("all"))

def on_mouse_drag(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def on_mouse_release(event):
    end_x, end_y = event.x, event.y
    extract_text(start_x, start_y, end_x, end_y)

def extract_text(x1, y1, x2, y2):
    global page_image
    # Asegura que las coordenadas estén ordenadas
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    # Recorta la región seleccionada
    cropped_image = page_image.crop((x1, y1, x2, y2))

    # Realiza OCR en la región seleccionada
    text = pytesseract.image_to_string(cropped_image)
    print("Texto reconocido:")
    print(text)

    # Muestra el texto en un cuadro de diálogo
    result_window = tk.Toplevel(root)
    result_window.title("Texto Reconocido")
    tk.Text(result_window, wrap="word", height=10, width=40).insert("1.0", text)

# Interfaz gráfica
root = tk.Tk()
root.title("Visualizador de PDF con OCR")

# Canvas para mostrar el PDF
canvas = tk.Canvas(root, width=800, height=600, bg="gray")
canvas.pack(fill="both", expand=True)

# Conexión de eventos de mouse
canvas.bind("<Button-1>", on_mouse_drag)  # Clic para iniciar selección
canvas.bind("<ButtonRelease-1>", on_mouse_release)  # Suelta el clic para finalizar

# Botón para seleccionar PDF
select_pdf_button = tk.Button(root, text="Cargar PDF", command=select_pdf)
select_pdf_button.pack(side="top", pady=10)

root.mainloop()
