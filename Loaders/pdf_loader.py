import PyPDF2  # To handle PDF files
from .abstract_loader import FileLoader  # Import the abstract FileLoader class
import os  # To handle file path operations

class PDFLoader(FileLoader):
    """
    A concrete class for loading and processing PDF files.

    This class inherits from the abstract FileLoader class and provides 
    implementation for validating and loading PDF files.

    Methods:
        validate_file(file_path): 
            Validates if the file exists and is a valid PDF file.

        load_file(file_path): 
            Loads the PDF file and extracts its text content.
            Handles encrypted PDFs as well.
    """

    def validate_file(self, file_path):
        """
        Validate if the provided file exists and if it is a valid PDF file.

        Parameters:
            file_path (str): The path to the PDF file to be validated.

        Returns:
            tuple: A tuple containing:
                - A boolean value indicating if the file is valid (True) or not (False).
                - A string message providing additional information about the validation result.
        
        Example:
            is_valid, message = pdf_loader.validate_file('path/to/file.pdf')
            if is_valid:
                print("File is valid")
            else:
                print(message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist."  # File doesn't exist
        if not file_path.endswith('.pdf'):
            return False, "Invalid file type. Expected a PDF file."  # Wrong file type
        return True, "File is valid."  # File exists and is valid

    def load_file(self, file_path):
        """
        Load the PDF file and extract its text content.

        Handles encrypted PDF files by attempting to decrypt them with an empty password.

        Parameters:
            file_path (str): The path to the PDF file to be loaded and processed.

        Returns:
            str: The extracted text content from the PDF file or an error message if any issue occurs.
        
        Raises:
            Exception: If there is an error during file loading.

        Example:
            content = pdf_loader.load_file('path/to/file.pdf')
            print(content)
        """
        try:
            # Open the PDF file in binary mode
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ""

                # Check if the PDF is encrypted
                if reader.is_encrypted:
                    # Attempt to decrypt with an empty password (some PDFs allow this)
                    if reader.decrypt("") == 0:
                        return "Error loading PDF: The file is password-protected."

                # Iterate through all pages and extract text
                for page in range(len(reader.pages)):
                    content += reader.pages[page].extract_text()

            return content  # Return the extracted content
        except Exception as e:
            return f"Error loading PDF: {e}"  # Return an error message if something goes wrong
