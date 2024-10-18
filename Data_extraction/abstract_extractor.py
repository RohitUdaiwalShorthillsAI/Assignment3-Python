from abc import ABC, abstractmethod

class DataExtractor(ABC):

    def __init__(self, file_loader):
        """
        Initialize the DataExtractor with a FileLoader instance.

        Parameters:
            file_loader (FileLoader): An instance of a file loader 
            (such as PDFLoader, DOCXLoader, or PPTLoader).
        """
        self.file_loader = file_loader

    @abstractmethod
    def extract_text(self):
        pass

    @abstractmethod
    def extract_links(self):
        pass

    @abstractmethod
    def extract_images(self):
        pass

    @abstractmethod
    def extract_tables(self):
        pass
