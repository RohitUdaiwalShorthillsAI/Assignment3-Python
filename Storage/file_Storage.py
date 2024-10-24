from abc import ABC, abstractmethod
import os
import csv
from Loaders.file_loader import FileLoader
from Data_extraction.file_extractor import FileDataExtractor

class FileStorage():
    def __init__(self, extractor, output_dir):
        """
        Initialize FileStorage with an extractor and output directory.

        :param extractor: An instance of the data extractor.
        :param output_dir: The directory where extracted data will be saved.
        """
        self.extractor = extractor
        self.output_dir = output_dir
        # Create the output directory if it does not exist
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self):
        """
        Save the extracted data (text, metadata, images, links, tables) to the specified output directory.
        """
        # Save extracted text
        text, metadata = self.extractor.extract_text()
        text_file_path = os.path.join(self.output_dir, 'extracted_text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

        # Save metadata to a separate file
        metadata_file_path = os.path.join(self.output_dir, "metadata.txt")
        with open(metadata_file_path, "w") as metadata_file:
            for key, value in metadata.items():
                metadata_file.write(f"{key}: {value}\n")

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
                    writer.writerow(row)  # Write each row of the table to the CSV file

        print(f"Data saved to file system in directory {self.output_dir}")
