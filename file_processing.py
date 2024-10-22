from Loaders.file_loader import FileLoader
from Data_extraction.file_extractor import FileDataExtractor
from Storage.file_Storage import FileStorage
from Storage.SQL_storage import MySQLStorage
from tabulate import tabulate


class FileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extractor = FileDataExtractor(self.file_path)

    def load_data(self):
        # Load the file content using the loader
        content = FileLoader.load_file(self.file_path)  # Ensure file_path is passed here as well
        print(content)
        return content

    def extract_data(self):
        # Extract and return data such as text, links, images, and tables
        data = {
            'text': self.extractor.extract_text(),
            'links': self.extractor.extract_links(),
            'images': self.extractor.extract_images(),
            'tables': self.extractor.extract_tables(),
        }
        return data

    def store_data(self, storage_type="file", storage_path=None):
        # Handle file storage or SQL storage based on user choice
        if storage_type == "file":
            if not storage_path:
                raise ValueError("Storage path is required for file storage.")
            storage = FileStorage(self.extractor, storage_path)
        else:
            storage = MySQLStorage(self.extractor)

        # Save the extracted data and close SQL storage if used
        storage.save()
        if storage_type == "sql":
            storage.close()

    def display_extracted_data(self, file_type, data):
        def display_metadata(metadata, allowed_keys):
            for key, value in metadata.items():
                if key in allowed_keys:
                    print(f"{key.capitalize()}: {value}")

        print(f"\n========== Extracted Data from {file_type.upper()} ==========\n")

        # Display text
        if 'text' in data:
            text, metadata = data['text']
            print("----- Extracted Text -----\n")
            print(text[:500] + '...' if len(text) > 500 else text)

        # Display metadata based on file type
        metadata_keys = {
            'pdf': ['author', 'title', 'subject', 'keywords', 'created', 'modified', 'producer'],
            'pptx': ['author', 'title', 'slide_count', 'created', 'last_modified_by', 'company', 'category'],
            'docx': ['author', 'title', 'revision', 'created', 'last_modified_by', 'word_count', 'character_count']
        }
        display_metadata(metadata, metadata_keys.get(file_type, []))

        # Display images with metadata according to file type
        if 'images' in data and data['images']:
            print(f"----- Extracted Images ({file_type.upper()}) -----\n")
            location_key = {'pptx': 'slide_number', 'pdf': 'page_number', 'docx': 'section'}  # updated key from 'pptx' to 'ppt'
            for idx, image in enumerate(data['images']):
                print(f"Image {idx + 1}: Format: {image['image_format']}, Resolution: {image['image_resolution']}, "
                    f"{location_key[file_type].capitalize()}: {image.get(location_key[file_type], 'N/A')}")
            print("\n")

        # Display links
        if 'links' in data and data['links']:
            print("----- Extracted Links -----\n")
            location_key = {'pptx': 'slide_number', 'pdf': 'page_number', 'docx': 'section'}
            for link in data['links']:
                print(f"URL: {link['url']} ({location_key[file_type].capitalize()} {link.get(location_key[file_type], 'N/A')})")
            print("\n")

        # Display tables
        if 'tables' in data and data['tables']:
            print(f"----- Extracted Tables ({file_type.upper()}) -----\n")
            for table_id, table in enumerate(data['tables']):
                print(f"Table {table_id + 1}:\n")
                print(tabulate(table, headers="firstrow", tablefmt="grid"))
                print("\n-----------------------------\n")

        print(f"========== End of Extraction for {file_type.upper()} ==========\n")

    @staticmethod
    def process_file(file_type, file_path, storage_type="file", storage_path=None):
        # Create a FileProcessor instance to handle the file processing
        processor = FileProcessor(file_path)
        print(f"Processing {file_type.upper()} file: {file_path}")

        # Load, extract, display, and store data
        processor.load_data()
        data = processor.extract_data()
        processor.display_extracted_data(file_type, data)
        processor.store_data(storage_type, storage_path)
        print(f"Data Stored Successfully ({storage_type.upper()})\n\n\n")
