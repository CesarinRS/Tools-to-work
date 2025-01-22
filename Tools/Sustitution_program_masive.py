"""
This script replace assigned page and adds it from the selected PDF files 
"""

import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog

# Hide the main window
root = tk.Tk()
root.withdraw()

# Request folder from the user 
folder_path = filedialog.askdirectory(
    title="Select the folder with the PDF files for the process "
)

if not folder_path:
    print("You didn't select a folder. The process has finished.")
    exit()

# Create a list of PDF files in the selected folder   
pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]

if not pdf_files:
    print("No PDF files found in the selected folder")
    exit()

# Request the user for the page number to replace  
page_to_replace = int(input("Enter the page number to replace (starting from 1): ")) - 1

# Request the PDF file with the new page
new_page_path = filedialog.askopenfilename(
    title="Select the PDF file with the new page:",
    filetypes=[("PDF files", "*.pdf")]
)

if not new_page_path:
    print("You didn't select file for the new page. The process has finished")
    exit()

# Read the new page from the selected file 
with open(new_page_path, "rb") as new_pdf_file:
    new_pdf_reader = PyPDF2.PdfReader(new_pdf_file)
    new_page = new_pdf_reader.pages[0]  # Assumes the file contains only one page

# Process each file in the folder
for pdf_path in pdf_files:
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            # Replace page at the indicated position
            for i, page in enumerate(pdf_reader.pages):
                if i == page_to_replace:
                    pdf_writer.add_page(new_page)
                    print(f"Page {page_to_replace + 1} replaced in '{os.path.basename(pdf_path)}'.")
                else:
                    pdf_writer.add_page(page)

            # Save the modified file
            output_path = os.path.join(folder_path, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_modified.pdf")
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

        print(f"File saved and modified: {output_path}")

    except Exception as e:
        print(f"Error processing '{pdf_path}': {e}")

print("Process complete successfully.")

