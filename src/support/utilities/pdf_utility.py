from PyPDF2 import PdfReader
from pdf2image import convert_from_path


def extract_text(path):
    return PdfReader(path).pages[0].extract_text()


def convert_pdf_to_jpg(pdf_path, jpg_path):
    pages = convert_from_path(pdf_path, 500)
    for page in pages:
        page.save(jpg_path, 'JPEG')
