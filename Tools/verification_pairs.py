"""
    This script verifies if the number of pages in selected PDF files is even or odd.
"""

import os
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog



# Function to select the folder with Tkinter
def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title="Select the folder with the PDFs")
    return folder_selected

# Function to check the PDFs and determine if number of pages is even or odd
def check_pdf_pages():
    folder = select_folder() # Call the function to select the folder
    

    # Verify if select folder exist
    if not os.path.exists(folder):
        print("The folder doesn't exist.")
    else:
        # Get a list of PDF files in folder
        files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
        # Check how many pages each PDF has
        for file in files:
            file_path = os.path.join(folder, file)
            
            try:
                with open(file_path, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    num_pages = len(pdf_reader.pages)

                    # Verify if number of pages is even or odd
                    if num_pages % 2 == 0:
                        print(f"{file} has an even number of pages ({num_pages} pages).")
                    else:
                        print(f"{file} has an odd number of pages ({num_pages} pages).")

            except Exception as e:
                print(f"Cannot read the PDF {file}: {e}")

# Execute the function
check_pdf_pages()


