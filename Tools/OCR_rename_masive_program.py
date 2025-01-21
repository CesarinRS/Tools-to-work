import pytesseract
from pdf2image import convert_from_path
from tkinter import Tk, Canvas
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk
import os
import shutil
import subprocess
import sys

# Instalar pdf2image y poppler si no están instalados
def install_pdf2image():
    try:
        import pdf2image
    except ImportError:
        print("pdf2image no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdf2image"])

    try:
        # Verificar si poppler está disponible, si no, instalarlo
        from pdf2image import pdfinfo_from_path
        print("pdf2image y poppler están instalados.")
    except ImportError:
        print("Poppler no está instalado, instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "poppler-utils"])

# Llamar a la función de instalación
install_pdf2image()

# Configura la ruta de Tesseract si no está en el PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Función para extraer texto usando OCR dentro de un área seleccionada
def extract_text_from_area(image, coords):
    cropped_image = image.crop(coords)  # Recortar la imagen
    text = pytesseract.image_to_string(cropped_image)  # Extraer texto
    return text.strip()

# Función para manejar el clic y arrastre del usuario en la interfaz gráfica
def on_drag(event):
    global x1, y1, x2, y2, rect
    x2, y2 = event.x, event.y
    canvas.coords(rect, x1, y1, x2, y2)  # Actualizar las coordenadas del rectángulo

def on_click(event):
    global x1, y1, rect
    x1, y1 = event.x, event.y
    rect = canvas.create_rectangle(x1, y1, x1, y1, outline='red', width=2)  # Crear el rectángulo inicial
    canvas.bind("<B1-Motion>", on_drag)  # Vincular el arrastre

    # Después de soltar el clic (botón izquierdo), finalizar la selección
    canvas.bind("<ButtonRelease-1>", on_release)

def on_release(event):
    global x2, y2
    x2, y2 = event.x, event.y
    canvas.unbind("<B1-Motion>")  # Dejar de seguir el arrastre
    canvas.unbind("<ButtonRelease-1>")  # Finalizar el proceso de selección
    print(f"Área seleccionada: ({x1}, {y1}) -> ({x2}, {y2})")  # Mostrar coordenadas en consola
    root.quit()  # Salir de la ventana

# Función para procesar todos los PDFs
def process_pdfs():
    # Seleccionar carpeta con PDFs
    input_folder = askdirectory(title="Selecciona la carpeta con los archivos PDF")
    if not input_folder:
        print("No se seleccionó ninguna carpeta.")
        return

    # Seleccionar carpeta de salida
    output_folder = askdirectory(title="Selecciona la carpeta para guardar los archivos procesados")
    if not output_folder:
        print("No se seleccionó ninguna carpeta de salida.")
        return

    # Obtener lista de archivos PDF
    pdf_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    if not pdf_paths:
        print("No se encontraron archivos PDF en la carpeta seleccionada.")
        return

    # Usar el primer archivo para seleccionar el área
    first_pdf = pdf_paths[0]
    pages = convert_from_path(first_pdf, first_page=1, last_page=1)  # Convertir primera página
    image = pages[0]

    # Ventana para seleccionar el área
    global root, canvas, x1, y1, x2, y2, rect
    root = Tk()
    canvas = Canvas(root, width=image.width, height=image.height)
    canvas.pack()

    # Convertir imagen a formato que Tkinter pueda mostrar
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")

    x1, y1, x2, y2 = None, None, None, None
    rect = None
    canvas.bind("<Button-1>", on_click)
    root.mainloop()  # Mostrar ventana hasta que se termine la selección

    # Validar si el área fue seleccionada
    if None in (x1, y1, x2, y2):
        print("No se seleccionó ninguna área.")
        return

    coords = (x1, y1, x2, y2)
    print(f"Coordenadas seleccionadas: {coords}")

    # Procesar todos los archivos en la carpeta
    for pdf_path in pdf_paths:
        pages = convert_from_path(pdf_path, first_page=1, last_page=1)  # Convertir primera página
        image = pages[0]

        # Extraer texto usando las mismas coordenadas
        extracted_text = extract_text_from_area(image, coords)
        if not extracted_text:
            print(f"No se pudo extraer texto del archivo: {pdf_path}")
            continue

        # Crear el nuevo nombre de archivo
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        new_name = f"{extracted_text}.pdf"
        output_path = os.path.join(output_folder, new_name)

        # Copiar el archivo original con el nuevo nombre
        shutil.copy(pdf_path, output_path)
        print(f"Archivo procesado: {pdf_path} -> {output_path}")

# Ejecutar el script
process_pdfs()
