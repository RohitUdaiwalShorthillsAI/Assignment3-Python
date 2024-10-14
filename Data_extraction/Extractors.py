from Loaders.pdf_loader import PDFLoader 
from Loaders.ppt_loader import PPTLoader
from Loaders.docx_loader import DOCXLoader 
from Data_extraction.abstract_extractor import DataExtractor
import fitz  # PyMuPDF for PDF handling
import docx  # python-docx for DOCX
import pptx  # python-pptx for PPTX
import io
from PIL import Image
import sqlite3

class PDFDataExtractor:
    def __init__(self, loader):
        self.loader = loader
        self.file_path = loader.file_path

    def extract_text(self):
        """Extract text and metadata from the PDF."""
        with fitz.open(self.file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        metadata = doc.metadata
        return text, metadata

    def extract_images(self):
        """Extract images from the PDF as BLOBs."""
        images = []
        with fitz.open(self.file_path) as doc:
            for page_num, page in enumerate(doc):
                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    img_resolution = f"{base_image['width']}x{base_image['height']}"
                    image_blob = sqlite3.Binary(image_bytes)
                    
                    images.append({
                        "image": image_blob,
                        "image_format": img_ext,
                        "image_resolution": img_resolution,
                        "page_number": page_num + 1
                    })
        return images

    def extract_tables(self):
        """Extract tables from the PDF (using pdfplumber)."""
        import pdfplumber
        tables = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                if extracted_tables:
                    for table in extracted_tables:
                        tables.append(table)
        return tables

    def extract_links(self):
        """Extract links from the PDF."""
        links = []
        with fitz.open(self.file_path) as doc:
            for page_num, page in enumerate(doc):
                for link in page.get_links():
                    links.append({
                        "url": link.get("uri", ""),
                        "page_number": page_num + 1
                    })
        return links


class DOCXDataExtractor:
    def __init__(self, loader):
        self.loader = loader
        self.file_path = loader.file_path

    def extract_text(self):
        """Extract text from DOCX file."""
        doc = docx.Document(self.file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        metadata = {}  # DOCX metadata isn't as readily available
        return text, metadata

    def extract_images(self):
        """Extract images from DOCX file as BLOBs."""
        images = []
        doc = docx.Document(self.file_path)
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image = rel.target_part.blob
                image_extension = rel.target_ref.split(".")[-1]
                img_resolution = "Unknown"
                image_blob = sqlite3.Binary(image)

                images.append({
                    "image": image_blob,
                    "image_format": image_extension,
                    "image_resolution": img_resolution,
                    "page_number": None  # DOCX files don't have "pages" in the same sense
                })
        return images

    def extract_tables(self):
        """Extract tables from DOCX file."""
        doc = docx.Document(self.file_path)
        tables = []
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            tables.append(table_data)
        return tables

    def extract_links(self):
        """Extract links from DOCX file."""
        links = []
        doc = docx.Document(self.file_path)
        
        # Iterate over all the paragraphs in the document
        for para in doc.paragraphs:
            # Check for hyperlinks in paragraph's relationships
            for rel in para._p.xpath('.//w:hyperlink'):
                rId = rel.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                if rId in para.part.rels:
                    link = para.part.rels[rId].target_ref
                    links.append({
                        "url": link,
                        "page_number": None  # DOCX files don't have pages
                    })
        return links


class PPTDataExtractor:
    def __init__(self, loader):
        self.loader = loader
        self.file_path = loader.file_path

    def extract_text(self):
        """Extract text from PPTX file."""
        presentation = pptx.Presentation(self.file_path)
        text = ""
        for slide_num, slide in enumerate(presentation.slides):
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        metadata = {}  # PPTX metadata can be accessed if necessary
        return text, metadata

    """Extract images from PPTX file as BLOBs."""
    def extract_images(self):
        images = []
        presentation = pptx.Presentation(self.file_path)
        
        # Loop over all slides
        for slide_num, slide in enumerate(presentation.slides):
            # Loop over all shapes in a slide
            for shape in slide.shapes:
                if hasattr(shape, "image") and shape.image:
                    # Extract image as BLOB
                    image_blob = io.BytesIO(shape.image.blob)
                    
                    # Read the image using PIL to get metadata
                    img = Image.open(image_blob)
                    image_format = img.format.lower()
                    
                    # Convert image to bytes for BLOB storage
                    image_bytes = io.BytesIO()
                    img.save(image_bytes, format=image_format.upper())
                    image_blob = sqlite3.Binary(image_bytes.getvalue())
                    
                    # Store image as BLOB in dictionary
                    images.append({
                        "image": image_blob,
                        "image_format": image_format,
                        "image_resolution": f"{img.width}x{img.height}",
                        "slide_number": slide_num + 1  # Use slide_number, not page_number
                    })
        return images


    def extract_tables(self):
        """Extract tables from PPTX file."""
        tables = []
        presentation = pptx.Presentation(self.file_path)
        for slide in presentation.slides:
            for shape in slide.shapes:
                if shape.has_table:
                    table_data = []
                    table = shape.table
                    for row in table.rows:
                        row_data = [cell.text.strip() for cell in row.cells]
                        table_data.append(row_data)
                    tables.append(table_data)
        return tables

    def extract_links(self):
        """Extract links from PPTX file."""
        links = []
        presentation = pptx.Presentation(self.file_path)
        for slide_num, slide in enumerate(presentation.slides):
            for shape in slide.shapes:
                if hasattr(shape, "hyperlink") and shape.hyperlink.address:
                    links.append({
                        "url": shape.hyperlink.address,
                        "slide_number": slide_num + 1
                    })
        return links
