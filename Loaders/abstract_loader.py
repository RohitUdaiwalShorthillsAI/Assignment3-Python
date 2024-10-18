from abc import ABC, abstractmethod

class FileLoader(ABC):
    """
    Abstract base class for file loaders.

    This class defines the structure for file loaders which are responsible 
    for validating and loading files of different formats such as PDF, DOCX, PPTX, etc.
    
    Methods:
        validate_file(file_path): 
            Abstract method to validate whether the file exists and is of the correct type.
            
        load_file(file_path): 
            Abstract method to load and process the contents of the file.
    """

    @abstractmethod
    def validate_file(self, file_path):
        """
        Validate if the file exists and is of the correct type.

        Parameters:
            file_path (str): The path to the file that needs to be validated.

        Returns:
            tuple: A tuple containing a boolean value indicating if the file is valid 
                   and a message indicating the validation result.
        """
        pass

    @abstractmethod
    def load_file(self, file_path):
        """
        Load and process the file.

        Parameters:
            file_path (str): The path to the file that needs to be loaded and processed.

        Returns:
            Any: The content of the file (this may vary depending on the file type).
            
        Raises:
            Exception: If there is an error loading the file.
        """
        pass
