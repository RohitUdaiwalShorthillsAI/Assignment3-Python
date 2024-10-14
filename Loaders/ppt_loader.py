from pptx import Presentation  # To handle PPT files
from .abstract_loader import FileLoader
import os

# PPT Loader
class PPTLoader(FileLoader):
    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            return False, "File does not exist."
        if not file_path.endswith('.pptx'):
            return False, "Invalid file type. Expected a PPTX file."
        return True, "File is valid."

    def load_file(self, file_path):
        try:
            presentation = Presentation(file_path)
            content = ""
            for slide in presentation.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        content += shape.text + "\n"
            return content
        except Exception as e:
            return f"Error loading PPT: {e}"