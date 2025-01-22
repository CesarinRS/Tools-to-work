"""
This script modifies a selected PDF file by rearranging its pages within the same file.
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
    filetypes=[("PDF Files", "*.pdf")]
)

if not main_pdf_path:
    print("You didn't select any file. The process has been terminated.")
    exit()

try:
    # Read the main PDF file
    pdf_reader = PyPDF2.PdfReader(main_pdf_path)
    total_pages = len(pdf_reader.pages)

    # Request the user to select the page number to move
    page_to_move = simpledialog.askinteger(
        "Page to Move",
        f"Select the page number to move (1-{total_pages}):",
        minvalue=1,
        maxvalue=total_pages
    )

    if not page_to_move:
        print("You didn't select any page. The process has been terminated.")
        exit()

    page_to_move_index = page_to_move - 1  # Adjust index (0-based)

    # Create a PdfWriter to construct the new file
    pdf_writer = PyPDF2.PdfWriter()

    # First, add the selected page to the beginning
    pdf_writer.add_page(pdf_reader.pages[page_to_move_index])
    print(f"Page {page_to_move} moved to the beginning.")

    # Then, add all other pages (except the selected one) in their original order
    for i in range(total_pages):
        if i != page_to_move_index:
            pdf_writer.add_page(pdf_reader.pages[i])

    # Save the modified file with a custom name
    base_name = os.path.splitext(os.path.basename(main_pdf_path))[0]
    output_filename = filedialog.asksaveasfilename(
        initialfile=f"{base_name}_modified.pdf",
        title="Save modified file as:",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not output_filename:
        print("The modified file wasn't saved.")
        exit()

    with open(output_filename, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"The modified file will be saved as: {output_filename}")

except Exception as e:
    print(f"Error processing the file: {e}")
print("Process completed successfully.")
