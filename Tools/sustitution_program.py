"""
This script replaces a page in a PDF file with another one.
"""

import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

# Hide the main Tkinter window
root = tk.Tk()
root.withdraw()

# Select the main PDF file
main_pdf_path = filedialog.askopenfilename(
    title="Select the main PDF file",
    filetypes=[("PDF files", "*.pdf")]
)

if not main_pdf_path:
    print("No file selected. The process has finished.")
    exit()

try:
    # Read the main PDF file
    pdf_reader = PyPDF2.PdfReader(main_pdf_path)
    total_pages = len(pdf_reader.pages)

    # Prompt the user to select the page number to replace
    page_to_replace = simpledialog.askinteger(
        "Page to Replace",
        f"Select the page number to replace (1-{total_pages}):",
        minvalue=1,
        maxvalue=total_pages
    )

    if not page_to_replace:
        print("No page selected. The process has finished.")
        exit()

    page_to_replace_index = page_to_replace - 1  # Adjust to zero-based index

    # Select the replacement PDF file
    replacement_pdf_path = filedialog.askopenfilename(
        title="Select the replacement PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not replacement_pdf_path:
        print("No replacement file selected. The process has finished.")
        exit()

    # Read the replacement PDF file
    replacement_pdf_reader = PyPDF2.PdfReader(replacement_pdf_path)
    replacement_total_pages = len(replacement_pdf_reader.pages)

    # Prompt the user to select the replacement page
    replacement_page = simpledialog.askinteger(
        "Select Replacement Page",
        f"Select the page number to use as replacement (1-{replacement_total_pages}):",
        minvalue=1,
        maxvalue=replacement_total_pages
    )

    if not replacement_page:
        print("No replacement page selected. The process has finished.")
        exit()

    replacement_page_index = replacement_page - 1  # Adjust to zero-based index

    # Create a PdfWriter to build the modified PDF
    pdf_writer = PyPDF2.PdfWriter()

    # Add all pages from the main PDF, replacing the selected page
    for i in range(total_pages):
        if i == page_to_replace_index:
            # Add the replacement page
            pdf_writer.add_page(replacement_pdf_reader.pages[replacement_page_index])
            print(f"Page {page_to_replace} in the main file has been replaced.")
        else:
            # Add the original page
            pdf_writer.add_page(pdf_reader.pages[i])

    # Save the modified file with a custom name
    base_name = os.path.splitext(os.path.basename(main_pdf_path))[0]
    output_filename = filedialog.asksaveasfilename(
        initialfile=f"{base_name}_modified.pdf",
        title="Save Modified File As:",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not output_filename:
        print("The modified file wasn't saved.")
        exit()

    with open(output_filename, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"The modified file has been saved as: {output_filename}")

except Exception as e:
    print(f"Processing error: {e}")

print("Process completed successfully.")

