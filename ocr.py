import sys
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ''


    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            try:
                text += f"\n--- Image {i+1} OCR result ---\n"
                text += pytesseract.image_to_string(image) + '\n'
            except Exception as e:
                print(f"Error processing image {i+1}: {str(e)}")
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")

    return text

def main():

    pdf_path = r"C:\Users\PC\Downloads\AI4I-CLAIMS-DATASET\Medical Quota share slip.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        sys.exit(1)

    try:
        print("Extracting text from PDF. This may take a few moments...")
        extracted_text = extract_text_from_pdf(pdf_path)
        print("Extracted text:")
        print(extracted_text)
        

        output_path = os.path.join(os.path.dirname(pdf_path), "extracted_text.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print(f"\nExtracted text has been saved to: {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()