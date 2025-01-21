import os
import PyPDF2

# Ruta de la carpeta donde están los archivos
folder_path = "C:\\Users\\auxmatla\\Downloads\\Requerimiento\\procesos\\fletes_pollo"

# Función para unir dos archivos PDF
def unir_pdfs(pdf1, pdf2, salida):
    pdf_writer = PyPDF2.PdfWriter()

    # Leer y agregar las páginas de ambos PDFs
    for archivo in [pdf1, pdf2]:
        try:
            pdf_reader = PyPDF2.PdfReader(archivo)
            for pagina in pdf_reader.pages:
                pdf_writer.add_page(pagina)
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")
            return False

    # Guardar el PDF combinado
    try:
        with open(salida, "wb") as archivo_salida:
            pdf_writer.write(archivo_salida)
        return True
    except Exception as e:
        print(f"Error al guardar {salida}: {e}")
        return False

# Obtener todos los archivos PDF en la carpeta
archivos_pdf = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

# Buscar coincidencias donde un archivo sea parte de otro
emparejados = {}
for archivo1 in archivos_pdf:
    for archivo2 in archivos_pdf:
        # Asegurarnos que no son el mismo archivo y verificar coincidencias
        if archivo1 != archivo2:
            # Comprobar si archivo1 está en archivo2
            if archivo1 in archivo2:
                # El archivo más largo debe ser el primero
                if len(archivo2) > len(archivo1):
                    emparejados[archivo2] = archivo1
                else:
                    emparejados[archivo1] = archivo2

# Unir los PDFs encontrados
for pdf1, pdf2 in emparejados.items():
    salida_nombre = f"{os.path.splitext(pdf1)[0]}_combinado.pdf"
    ruta_pdf1 = os.path.join(folder_path, pdf1)
    ruta_pdf2 = os.path.join(folder_path, pdf2)
    ruta_salida = os.path.join(folder_path, salida_nombre)

    if unir_pdfs(ruta_pdf1, ruta_pdf2, ruta_salida):
        print(f"Combinado: {pdf1} + {pdf2} -> {salida_nombre}")

print("Proceso completado.")
