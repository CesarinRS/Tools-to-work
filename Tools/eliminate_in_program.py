import PyPDF2
import os

# Especifica la ruta a la carpeta que contiene los PDFs
folder_path = "C:\\Users\\auxmatla\\Downloads\\prueba\\reenombrado"
# Especifica la ruta donde se guardarán los PDFs modificados
output_folder = "C:\\Users\\auxmatla\\Downloads\\prueba\\eliminado-bueno-2"

# Crea la carpeta de destino si no existe
os.makedirs(output_folder, exist_ok=True)

# Itera sobre cada archivo en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)

        # Crea un lector y escritor de PDF
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        pdf_writer = PyPDF2.PdfWriter()

        # Itera sobre las páginas del PDF
        for page_num in range(len(pdf_reader.pages)):
            if page_num != 1:  # Elimina la segunda página (la pagina 1 es el índice 0)
                pdf_writer.add_page(pdf_reader.pages[page_num])

        # Define la ruta y nombre del nuevo archivo (sin prefijo adicional)
        output_path = os.path.join(output_folder, filename)

        # Guarda el nuevo archivo PDF
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

        print(f"Se ha guardado: {output_path}")

print("Las páginas han sido eliminadas y los archivos han sido guardados.")
