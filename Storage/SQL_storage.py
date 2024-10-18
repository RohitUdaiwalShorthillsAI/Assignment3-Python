import mysql.connector
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

# Abstract Class: Storage
class Storage(ABC):
    def __init__(self, extractor):
        """
        Initialize the Storage class with a data extractor and establish a MySQL database connection.

        :param extractor: An instance of the data extractor to be used for data extraction.
        """
        load_dotenv()
        
        self.extractor = extractor
        self.conn = mysql.connector.connect(
            host= os.getenv('DB_HOST'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD'),
            database= os.getenv('DB_'),  # MySQL database name
            auth_plugin='mysql_native_password'  # Use the native authentication plugin
        )

    @abstractmethod
    def save(self):
        """Save the extracted data to the database."""
        pass

class MySQLStorage(Storage):
    table_name = 1
    def __init__(self, extractor):
        """
        Initialize MySQLStorage with an extractor and create necessary database tables.

        :param extractor: An instance of the data extractor.
        """
        super().__init__(extractor)
        self.cursor = self.conn.cursor()  # Create a cursor to interact with the database
        self.create_tables()  # Create tables if they don't exist

    def create_tables(self):
        """
        Create tables for storing extracted text, links, images, and tables in the MySQL database.
        The tables are created if they do not already exist.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_text (content TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_links (link TEXT, page_number INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_images (image LONGBLOB, image_format TEXT, resolution TEXT, page_number INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_tables (table_id INTEGER, row_data TEXT)''')
        self.conn.commit()  # Commit the table creation to the database

    def save(self):
        """
        Save the extracted data (text, links, images, tables) to the MySQL database.
        This method performs the following operations:
        - Save extracted text
        - Save extracted links
        - Save extracted images
        - Save extracted tables
        """
        # Save extracted text
        text_content, _ = self.extractor.extract_text()  # Extract the text, discard metadata
        if text_content:  # Only insert if there is text data
            self.cursor.execute('INSERT INTO extracted_text (content) VALUES (%s)', (text_content,))
        
        # Save extracted links
        links = self.extractor.extract_links()  # Extract links from the document
        for link in links:
            self.cursor.execute('INSERT INTO extracted_links (link, page_number) VALUES (%s, %s)', 
                                (link['url'], link.get('page_number', link.get('slide_number'))))  # Insert links into the database

        # Save extracted images
        images = self.extractor.extract_images()
        for img in images:
            # Convert the memoryview object to bytes before saving to MySQL
            img_data = bytes(img['image'])  # Convert memoryview to bytes
            # Use 'slide_number' instead of 'page_number' for PPTX files
            self.cursor.execute('INSERT INTO extracted_images (image, image_format, resolution, page_number) VALUES (%s, %s, %s, %s)',
                                (img_data, img['image_format'], img['image_resolution'], img.get('page_number', img.get('slide_number'))))

        
        # Save extracted tables
        tables = self.extractor.extract_tables()  # Extract tables from the document
        for table_id, table in enumerate(tables):
            if not table:  # Skip empty tables
                continue

            # Get the column names from the first row
            column_names = table[0]

            # Sanitize column names for SQL compatibility (replace spaces and other special characters)
            sanitized_columns = []
            for col in column_names:
                sanitized_col = col.strip().replace(" ", "_").replace("-", "_").replace(".", "_")
                sanitized_columns.append(sanitized_col)

            # Create a new SQL table for each extracted table
            table_name = f'extracted_table_{MySQLStorage.table_name}'  # Unique table name for each table
            MySQLStorage.table_name += 1
            
            # Prepare the column definitions for table creation
            sanitized_column_defs = [f'`{col}` TEXT' for col in sanitized_columns]
            
            # Check if the table already exists
            try:
                self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                result = self.cursor.fetchone()

                if result:  # Table exists
                    print(f"Table {table_name} already exists. Skipping creation.")

                    # Check the existing columns in the table
                    self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    existing_columns = [col[0] for col in self.cursor.fetchall()]

                    # Check for columns that need to be added
                    for col in sanitized_columns:
                        if col not in existing_columns:
                            alter_query = f"ALTER TABLE {table_name} ADD COLUMN `{col}` TEXT"
                            self.cursor.execute(alter_query)
                            print(f"Added column `{col}` to table {table_name}.")

                else:  # Create the table if it doesn't exist
                    create_table_query = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join(sanitized_column_defs)})"
                    self.cursor.execute(create_table_query)
                    print(f"Table created: {table_name}")

            except mysql.connector.Error as err:
                print(f"Error checking/creating table {table_name}: {err}")
                continue  # Skip to the next table if there's an error

            # Prepare the column names for insertion (same as headers without data types)
            column_names_for_insert = [f'`{col}`' for col in sanitized_columns]

            # Insert the remaining rows (skip the first row as it contains headers)
            for row in table[1:]:
                try:
                    # Dynamically build the SQL query for inserting data
                    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names_for_insert)}) VALUES ({', '.join(['%s'] * len(row))})"
                    self.cursor.execute(insert_query, tuple(row))  # Insert the row into the table
                except mysql.connector.Error as err:
                    print(f"Error inserting into table {table_name}: {err} for row: {row}")
                    continue  # Skip to the next row if there's an error

        # Commit the transaction after all inserts
        self.conn.commit()



        print(f"Data saved to MySQL database")  # Confirmation message

    def close(self):
        """Close the database connection to free up resources."""
        self.conn.close()
