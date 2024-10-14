from abc import ABC, abstractmethod
import os
import csv
# import sqlite3
from Data_extraction.Extractors import PDFDataExtractor
from Data_extraction.Extractors import PPTDataExtractor
from Data_extraction.Extractors import DOCXDataExtractor
from Loaders.pdf_loader import PDFLoader
from Loaders.ppt_loader import PPTLoader
from Loaders.docx_loader import DOCXLoader

#Abstract - Class: Storage
class Storage(ABC):
    def __init__(self, extractor):
        self.extractor = extractor

    @abstractmethod
    def save(self):
        """Save the extracted data."""
        pass


class FileStorage(Storage):
    def __init__(self, extractor, output_dir):
        super().__init__(extractor)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self):
        # Save extracted text
        text, metadata = self.extractor.extract_text()
        text_file_path = os.path.join(self.output_dir, 'extracted_text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

        # Save extracted links
        links = self.extractor.extract_links()
        links_file_path = os.path.join(self.output_dir, 'extracted_links.txt')
        with open(links_file_path, 'w', encoding='utf-8') as links_file:
            for link in links:
                links_file.write(f"{link['url']} (Page/Slide: {link.get('page_number', link.get('slide_number'))})\n")

        # Save extracted images
        images = self.extractor.extract_images()
        images_dir = os.path.join(self.output_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        for idx, img in enumerate(images):
            image_file_path = os.path.join(images_dir, f'image_{idx+1}.{img["image_format"]}')
            with open(image_file_path, 'wb') as image_file:
                image_file.write(img['image'])

        # Save extracted tables to CSV files
        tables = self.extractor.extract_tables()
        for table_id, table in enumerate(tables):
            table_file_path = os.path.join(self.output_dir, f'table_{table_id+1}.csv')
            with open(table_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                for row in table:
                    writer.writerow(row)

        print(f"Data saved to file system in directory {self.output_dir}")


