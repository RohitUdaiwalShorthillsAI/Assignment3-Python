from abc import ABC, abstractmethod


class FileLoader(ABC):
    @abstractmethod
    def validate_file(self, file_path):
        """Validate if the file exists and is of the correct type."""
        pass

    @abstractmethod
    def load_file(self, file_path):
        """Load and process the file."""
        pass
