# Assignment3-Python

# File Data Extraction and Storage System

This repository provides a Python-based solution to extract text, hyperlinks, images, and tables from PDF, DOCX, and PPT files with metadata and store the extracted data either in files or in an SQL database.

## Project Overview

The project is designed as a modular system with clear separation of responsibilities, providing flexibility to extend or modify its components. The main components of the system are:

1. **File Loading**: Loads PDF, DOCX, or PPT files for processing.
2. **Data Extraction**: Extracts text, links, images, and tables, while capturing relevant metadata (e.g., page number, resolution).
3. **Storage**: Saves extracted data either to files or an SQL database.

## Features

- **Text Extraction**: Extracts text along with metadata such as page numbers, font styles, and headings.
- **Link Extraction**: Extracts hyperlinks and related metadata (e.g., linked text, URL, page number).
- **Image Extraction**: Extracts images along with metadata like resolution, format, and page numbers.
- **Table Extraction**: Extracts tables and provides their dimensions and page number.
- **Storage**: Saves extracted data to a local directory (as text, CSV, or image files) or stores the data in an SQL database.

## Class Structure

### 1. **FileLoader (Abstract Class)**

Defines the interface for validating and loading files.

- `validate_file(file_path)`: Ensures the file exists and is of the correct type.
- `load_file(file_path)`: Loads the file for further processing.

### 2. **Concrete FileLoader Classes**
These classes implement specific file-loading logic for each file type.

- **PDFLoader**: Handles PDF files using `PyPDF2`.
- **DOCXLoader**: Handles DOCX files using `python-docx`.
- **PPTLoader**: Handles PPT files using `python-pptx`.

### 3. **DataExtractor Class**

This class takes a `FileLoader` instance as input and provides methods to extract data:

- `extract_text()`: Extracts text from the document along with metadata.
- `extract_links()`: Extracts hyperlinks and associated metadata.
- `extract_images()`: Extracts images and metadata like resolution and format.
- `extract_tables()`: Extracts tables and metadata like dimensions.

### 4. **Storage (Abstract Class)**

Defines the interface for saving extracted data. Two concrete implementations are provided:

- **FileStorage**: Saves extracted data to local files (e.g., images to directories, tables to CSV).
- **SQLStorage**: Stores extracted data in an SQL database.
