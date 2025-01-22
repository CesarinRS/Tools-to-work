"""
This script merges the PDF files selected by the user into a single document
"""

import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog

# Hide the main window
root = tk.Tk()
root.withdraw()

# Window for selecting PDF files to merge
pdf_paths = filedialog.askopenfilenames(
    title="Select PDF files for merge",
    filetypes=[("PDF Files", "*.pdf")]
)

if not pdf_paths:
    print("You didn't select any files. The process has finished.")
    exit()

# Window for saving the new combined PDF file with a custom name "Save combined PDF file as"
output_filename = filedialog.asksaveasfilename(
    initialdir=os.path.join(os.path.expanduser("~"), "Downloads"),
    title="Save combined PDF file as",
    defaultextension=".pdf",
    filetypes=[("PDF Files", "*.pdf")]
)

if not output_filename:
    print("You didn't select a name for the file. The process has finished.")
    exit()

# Create a PdfWriter to combine pages
pdf_writer = PyPDF2.PdfWriter()

# Add pages from selected PDF files in the chosen order
for pdf_path in pdf_paths:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        print(f"Added: {os.path.basename(pdf_path)}")
    except Exception as e:
        print(f"Error processing '{os.path.basename(pdf_path)}': {e}")

# Save the combined PDF file with the user-specified name 
with open(output_filename, "wb") as output_file:
    pdf_writer.write(output_file)

print(f"Combined PDF saved at: {output_filename}")  
print("Process completed.")
 
