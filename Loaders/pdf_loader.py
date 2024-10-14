import PyPDF2  # To handle PDF files
from .abstract_loader import FileLoader
import os

class PDFLoader(FileLoader):
    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            return False, "File does not exist."
        if not file_path.endswith('.pdf'):
            return False, "Invalid file type. Expected a PDF file."
        return True, "File is valid."

    def load_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ""
                for page in range(len(reader.pages)):
                    content += reader.pages[page].extract_text()
            return content
        except Exception as e:
            return f"Error loading PDF: {e}"