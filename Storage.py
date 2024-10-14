from abc import ABC, abstractmethod
import os
import csv
import sqlite3
from Extractors import PDFDataExtractor
from Loaders import PDFLoader

# Abstract Class: Storage
class Storage(ABC):
    def __init__(self, extractor):
        self.extractor = extractor

    @abstractmethod
    def save(self):
        """Save the extracted data."""
        pass

# Concrete Class: FileStorage
class FileStorage(Storage):
    def __init__(self, extractor, output_dir):
        super().__init__(extractor)
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save(self):
        """Save extracted text, images, links, and tables to files."""
        # Save text to file
        text = self.extractor.extract_text()
        text_file = os.path.join(self.output_dir, 'extracted_text.txt')
        with open(text_file, 'w') as f:
            f.write(str(text))
        print(f"Text saved to {text_file}")

        # Save hyperlinks to file
        links = self.extractor.extract_links()
        links_file = os.path.join(self.output_dir, 'extracted_links.txt')
        with open(links_file, 'w') as f:
            for link in links:
                f.write(f"{link}\n")
        print(f"Links saved to {links_file}")

        # Save images to directory
        images = self.extractor.extract_images()
        image_dir = os.path.join(self.output_dir, 'images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        for i, img in enumerate(images):
            image_path = os.path.join(image_dir, f'image_{i}.png')
            with open(image_path, 'wb') as f:  # Write in binary mode ('wb')
                f.write(img)  # `img` should be binary data

        # Save tables to CSV files
        tables = self.extractor.extract_tables()
        for idx, table in enumerate(tables):
            table_file = os.path.join(self.output_dir, f'table_{idx}.csv')
            with open(table_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(table)
        print(f"Tables saved to CSV files in {self.output_dir}")

# Concrete Class: SQLStorage
class SQLStorage(Storage):
    def __init__(self, extractor, db_path):
        super().__init__(extractor)
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables for text, links, images, and tables in the SQL database."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_text (content TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_links (link TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_images (image BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_tables (table_id INTEGER, row_data TEXT)''')
        self.connection.commit()

    def save(self):
        """Store extracted text, links, images, and tables in the SQL database."""
        # Save extracted text
        text = self.extractor.extract_text()
        self.cursor.execute('INSERT INTO extracted_text (content) VALUES (?)', (text,))
        
        # Save extracted links
        links = self.extractor.extract_links()
        for link in links:
            self.cursor.execute('INSERT INTO extracted_links (link) VALUES (?)', (link,))
        
        # Save extracted images
        images = self.extractor.extract_images()
        for img in images:
            self.cursor.execute('INSERT INTO extracted_images (image) VALUES (?)', (sqlite3.Binary(img),))
        
        # Save extracted tables
        tables = self.extractor.extract_tables()
        for table_id, table in enumerate(tables):
            for row in table:
                row_data = ','.join(row)
                self.cursor.execute('INSERT INTO extracted_tables (table_id, row_data) VALUES (?, ?)', (table_id, row_data))
        
        self.connection.commit()
        print(f"Data saved to SQL database at {self.db_path}")

    def close(self):
        """Close the database connection."""
        self.connection.close()


    # Create an instance of DataExtractor
pdf_loader = PDFLoader()
pdf_loader.file_path = 'Document.pdf'  # PDF file path
extractor = PDFDataExtractor(pdf_loader)

# Use FileStorage to save the extracted data to the file system
file_storage = FileStorage(extractor, './output')

# Save the data to the file system
file_storage.save()

# The extracted text, images, links, and tables will be saved in the 'output' directory.
# - 'extracted_text.txt' will contain the extracted text.
# - 'extracted_links.txt' will contain the links.
# - 'images' directory will store the images as .png files.
# - 'table_0.csv' and 'table_1.csv' will contain the extracted tables.

