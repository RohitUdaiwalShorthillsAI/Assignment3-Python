import docx    # To handle DOCX files
from .abstract_loader import FileLoader
import os

# DOCX Loader
class DOCXLoader(FileLoader):
    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            return False, "File does not exist."
        if not file_path.endswith('.docx'):
            return False, "Invalid file type. Expected a DOCX file."
        return True, "File is valid."

    def load_file(self, file_path):
        try:
            doc = docx.Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
            return content
        except Exception as e:
            return f"Error loading DOCX: {e}"