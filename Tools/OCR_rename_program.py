import pytesseract
from pdf2image import convert_from_path
from tkinter import Tk, Canvas
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from PIL import Image
import os

# Configura la ruta de tesseract si no está en el PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Función para extraer texto usando OCR dentro de un área seleccionada
def extract_text_from_area(image, coords):
    # Recorta la imagen usando las coordenadas
    cropped_image = image.crop(coords)
    # Convierte la imagen recortada a texto usando pytesseract
    text = pytesseract.image_to_string(cropped_image)
    return text.strip()

# Función para manejar el clic del usuario en la interfaz gráfica
def on_click(event):
    global x1, y1, x2, y2
    # Primer clic: marca la esquina superior izquierda
    if x1 is None and y1 is None:
        x1, y1 = event.x, event.y
    # Segundo clic: marca la esquina inferior derecha
    else:
        x2, y2 = event.x, event.y
        canvas.create_rectangle(x1, y1, x2, y2, outline='red')  # Dibuja el rectángulo
        root.quit()  # Termina la selección

# Función para seleccionar el archivo y procesarlo
def process_pdfs():
    # Abrir el selector de archivos PDF
    pdf_paths = askopenfilenames(filetypes=[("Archivos PDF", "*.pdf")])
    
    if not pdf_paths:
        print("No se seleccionaron archivos PDF.")
        return

    # Cargar la primera página del primer archivo PDF como imagen
    pdf_path = pdf_paths[0]  # Solo usar el primer archivo para la selección
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)  # Convierte la primera página a imagen
    image = pages[0]  # Obtener la imagen de la primera página
    
    # Crear una ventana para seleccionar el área de texto
    global root, canvas, x1, y1, x2, y2
    root = Tk()
    canvas = Canvas(root, width=image.width, height=image.height)
    canvas.pack()
    
    # Convertir la imagen a formato que Tkinter pueda mostrar
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")
    
    x1, y1, x2, y2 = None, None, None, None
    canvas.bind("<Button-1>", on_click)
    root.mainloop()

    # Extraer el texto de la región seleccionada
    if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
        coords = (x1, y1, x2, y2)
        extracted_text = extract_text_from_area(image, coords)
        print("Texto extraído:", extracted_text)
        
        # Renombrar archivos con el texto extraído o crear una copia
        for pdf_path in pdf_paths:
            base_name = os.path.basename(pdf_path)
            new_name = f"{extracted_text}.pdf"
            new_path = asksaveasfilename(initialfile=new_name, defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])

            if new_path:
                # Aquí puedes agregar la lógica para guardar el archivo renombrado
                # Copiar el archivo con el nuevo nombre (si se desea copiar y no renombrar)
                os.rename(pdf_path, new_path)
                print(f"Archivo renombrado/copiado a: {new_path}")

    else:
        print("No se seleccionó ninguna área.")

# Llamar la función para iniciar el proceso
process_pdfs()
