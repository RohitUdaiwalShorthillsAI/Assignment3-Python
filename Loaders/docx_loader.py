import docx  # To handle DOCX files
from .abstract_loader import FileLoader  # Import the abstract FileLoader class
import os  # To handle file path operations

# DOCX Loader
class DOCXLoader(FileLoader):
    """
    A concrete class for loading and processing DOCX files.

    This class inherits from the abstract FileLoader class and provides 
    implementation for validating and loading DOCX files.
    
    Methods:
        validate_file(file_path): 
            Validates if the file exists and if it is a valid DOCX file.
            
        load_file(file_path): 
            Loads the DOCX file and extracts its text content.
    """

    def validate_file(self, file_path):
        """
        Validate if the provided file exists and if it is a valid DOCX file.

        Parameters:
            file_path (str): The path to the DOCX file to be validated.

        Returns:
            tuple: A tuple containing:
                - A boolean value indicating if the file is valid (True) or not (False).
                - A string message providing additional information about the validation result.
        
        Example:
            is_valid, message = docx_loader.validate_file('path/to/file.docx')
            if is_valid:
                print("File is valid")
            else:
                print(message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist."  # File doesn't exist
        if not file_path.endswith('.docx'):
            return False, "Invalid file type. Expected a DOCX file."  # Wrong file type
        return True, "File is valid."  # File exists and is valid

    def load_file(self, file_path):
        """
        Load the DOCX file and extract its text content.

        Parameters:
            file_path (str): The path to the DOCX file to be loaded and processed.

        Returns:
            str: The extracted text content from the DOCX file.

        Raises:
            Exception: If there is an error during file loading.

        Example:
            content = docx_loader.load_file('path/to/file.docx')
            print(content)
        """
        try:
            doc = docx.Document(file_path)  # Load the DOCX file using the docx module
            # Extract text from each paragraph and join them with newlines
            content = "\n".join([para.text for para in doc.paragraphs])
            return content
        except Exception as e:
            return f"Error loading DOCX: {e}"  # Return an error message if something goes wrong
