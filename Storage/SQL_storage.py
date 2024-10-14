from abc import ABC, abstractmethod
import os
import sqlite3
from Data_extraction.Extractors import PDFDataExtractor, PPTDataExtractor, DOCXDataExtractor
from Loaders.pdf_loader import PDFLoader
from Loaders.ppt_loader import PPTLoader
from Loaders.docx_loader import DOCXLoader

# Abstract Class: Storage
class Storage(ABC):
    def __init__(self, extractor):
        self.extractor = extractor

    @abstractmethod
    def save(self):
        """Save the extracted data."""
        pass

class SQLStorage(Storage):
    def __init__(self, extractor, db_path):
        super().__init__(extractor)
        self.db_path = db_path

        # Ensure output directory exists if db_path includes a directory
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Check if there's a directory in the path
            os.makedirs(db_dir, exist_ok=True)

        # Initialize SQLite database connection
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables for text, links, images, and tables in the SQL database."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_text (content TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_links (link TEXT, page_number INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_images (image BLOB, image_format TEXT, resolution TEXT, page_number INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_tables (table_id INTEGER, row_data TEXT)''')
        self.connection.commit()

    def save(self):
        # Save extracted text
        text, _ = self.extractor.extract_text()
        if text:  # Only insert if there is text data
            self.cursor.execute('INSERT INTO extracted_text (content) VALUES (?)', (text,))
        
        # Save extracted links
        links = self.extractor.extract_links()
        for link in links:
            self.cursor.execute('INSERT INTO extracted_links (link, page_number) VALUES (?, ?)', 
                                (link['url'], link.get('page_number', link.get('slide_number'))))

        # Save extracted images
        images = self.extractor.extract_images()
        for img in images:
            self.cursor.execute('INSERT INTO extracted_images (image, image_format, resolution, page_number) VALUES (?, ?, ?, ?)',
                                (sqlite3.Binary(img['image']), img['image_format'], img['image_resolution'], img['page_number']))
        
        # Save extracted tables (this assumes the tables are returned as lists of lists)
        tables = self.extractor.extract_tables()
        for table_id, table in enumerate(tables):
            for row in table:
                row_data = ','.join(row)  # Convert the row to a comma-separated string
                self.cursor.execute('INSERT INTO extracted_tables (table_id, row_data) VALUES (?, ?)', (table_id, row_data))

        self.connection.commit()
        print(f"Data saved to SQL database at {self.db_path}")

    def close(self):
        """Close the database connection."""
        self.connection.close()
