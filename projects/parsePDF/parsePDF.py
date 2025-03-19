import PyPDF2
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pdf2image import convert_from_path
import pytesseract

# Specify the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Hide the main Tkinter window
Tk().withdraw()

# Prompt user to select a PDF file through the file explorer
pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

# Verify the user selected a file
if not pdf_path:
    print("No file selected.")
    exit()

try:
    # Attempt to extract text using PyPDF2
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                extracted_text += text

    # If PyPDF2 extraction yields no text, fall back to OCR
    if not extracted_text.strip():
        print("No text detected using PyPDF2, falling back to OCR...")
        pages = convert_from_path(pdf_path, dpi=300)
        extracted_text = ""

        for page in pages:
            extracted_text += pytesseract.image_to_string(page)

    # Output extracted text to console
    print("\nExtracted Text:\n")
    print(extracted_text)

    # Define the output path (Downloads folder)
    downloads_folder = os.path.expanduser("~/Downloads")
    output_file_path = os.path.join(downloads_folder, "extracted_text.txt")

    # Save extracted text to the Downloads folder
    with open(output_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    print(f"\nExtracted text saved to: {output_file_path}")

except FileNotFoundError:
    print("The file was not found.")
except PyPDF2.errors.PdfReadError:
    print("The file is not a valid PDF or is corrupted.")
except Exception as e:
    print(f"An error occurred: {e}")
