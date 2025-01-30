"""
This script takes the first selected PDF file and inserts it into another PDF file.
"""

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
        messagebox.showerror("Error", "The position is not valid. It must be an integer number.")
        return

    if not pdf1_path or not pdf2_path:
        messagebox.showerror("Error", "Both PDF files must be selected.")
        return

    try:
        # Read PDF files
        pdf1_reader = PdfReader(pdf1_path)
        pdf2_reader = PdfReader(pdf2_path)
        pdf_writer = PdfWriter()

        # Validate position
        if insert_position < 1 or insert_position > len(pdf1_reader.pages):
            messagebox.showerror("Error", "The selected range is not valid.")
            return

        # Add pages from PDF1 up to the insert position
        for i in range(insert_position - 1):
            pdf_writer.add_page(pdf1_reader.pages[i])

        # Add all pages from PDF2
        for page in pdf2_reader.pages:
            pdf_writer.add_page(page)

        # Add the remaining pages from PDF1
        for i in range(insert_position - 1, len(pdf1_reader.pages)):
            pdf_writer.add_page(pdf1_reader.pages[i])

        # Save the combined PDF
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)
            messagebox.showinfo("Success", "PDF files have been successfully combined.")
    except Exception as e:
        messagebox.showerror("Error", f"Error processing files: {e}")

# Create GUI
root = tk.Tk()
root.title("Insert PDF into another PDF")

# Widgets for PDF1
label_pdf1 = tk.Label(root, text="Select PDF 1:")
label_pdf1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_pdf1 = tk.Entry(root, width=50)
entry_pdf1.grid(row=0, column=1, padx=10, pady=5)
button_pdf1 = tk.Button(root, text="Browse", command=select_pdf1)
button_pdf1.grid(row=0, column=2, padx=10, pady=5)

# Widgets for PDF2
label_pdf2 = tk.Label(root, text="Select PDF 2:")
label_pdf2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_pdf2 = tk.Entry(root, width=50)
entry_pdf2.grid(row=1, column=1, padx=10, pady=5)
button_pdf2 = tk.Button(root, text="Browse", command=select_pdf2)
button_pdf2.grid(row=1, column=2, padx=10, pady=5)

# Widgets for position
label_position = tk.Label(root, text="Insert position (Insert after the specified page number):")
label_position.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_position = tk.Entry(root, width=10)
entry_position.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Combine PDFs button
button_merge = tk.Button(root, text="Combine PDFs", command=merge_pdfs)
button_merge.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()

