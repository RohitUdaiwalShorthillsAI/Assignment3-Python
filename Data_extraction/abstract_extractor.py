from abc import ABC, abstractmethod

class DataExtractor(ABC):
    def __init__(self, file_loader):
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