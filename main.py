from Loaders.pdf_loader import PDFLoader
from Loaders.docx_loader import DOCXLoader
from Loaders.ppt_loader import PPTLoader
from Data_extraction.Extractors import PDFDataExtractor
from Data_extraction.Extractors import DOCXDataExtractor
from Data_extraction.Extractors import PPTDataExtractor
from Storage.file_Storage import FileStorage
from Storage.SQL_storage import SQLStorage

# # 1.Test Example for Loading the data -

# pdf_loader = PDFLoader()
# docx_loader = DOCXLoader()
# ppt_loader = PPTLoader()

# # PDF File Example
# is_valid, message = pdf_loader.validate_file('Samples/Sample_file.pdf')
# if is_valid:
#     pdf_content = pdf_loader.load_file('Samples/Sample_file.pdf')
#     print("PDF Content:", pdf_content)
# else:
#     print(message)

# # DOCX File Example
# is_valid, message = docx_loader.validate_file('Samples/Sample_file.docx')
# if is_valid:
#     docx_content = docx_loader.load_file('Samples/Sample_file.docx')
#     print("DOCX Content:", docx_content)
# else:
#     print(message)

# # PPT File Example
# is_valid, message = ppt_loader.validate_file('Samples/Sample_file.pptx')
# if is_valid:
#     ppt_content = ppt_loader.load_file('Samples/Sample_file.pptx')
#     print("PPT Content:", ppt_content)
# else:
#     print(message)


# # 2. Test Example for Extracting the data -

# # i. For Pdf 
# pdf_loader = PDFLoader()
# pdf_loader.file_path = 'Samples/Sample_file.pdf'  # PDF file path
# pdf_extractor = PDFDataExtractor(pdf_loader)

# # # Extract text and metadata from PDF
# pdf_text, pdf_text_metadata = pdf_extractor.extract_text()
# print("PDF Text:", pdf_text)
# print("PDF Metadata:", pdf_text_metadata)

# # ii. For Docx
# docx_loader = DOCXLoader()
# docx_loader.file_path = 'Samples/Sample_file.docx'  # DOCX file path
# docx_extractor = DOCXDataExtractor(docx_loader)

# # Extract tables from DOCX
# docx_tables_metadata = docx_extractor.extract_tables()
# print("DOCX Tables Metadata:", docx_tables_metadata)

# # iii. For Ppt
# ppt_loader = PPTLoader()
# ppt_loader.file_path = 'Samples/Sample_file.pptx'  # PPTX file path
# ppt_extractor = PPTDataExtractor(ppt_loader)

# # Extract images from PPT
# ppt_images_metadata = ppt_extractor.extract_images()
# print("PPT Images Metadata:", ppt_images_metadata)


# 3. Test Example for Storing Data

# # i. For Pdf
# pdf_loader = PDFLoader()
# pdf_loader.file_path = 'Samples/Sample_file.pdf'  # PDF file path
# pdf_extractor = PDFDataExtractor(pdf_loader)

# # File storage example
# file_storage = FileStorage(pdf_extractor, './output/pdf_files')
# file_storage.save()

# # SQL storage example
# sql_storage = SQLStorage(pdf_extractor, './output/SQL_DB_PDF.db')
# sql_storage.save()
# sql_storage.close()


# ii. For Docx
docx_loader = DOCXLoader()
docx_loader.file_path = 'Samples/Sample_file.docx'  # PDF file path
docx_extractor = DOCXDataExtractor(docx_loader)

# File storage example
file_storage = FileStorage(docx_extractor, './output/docx_files')
file_storage.save()

# SQL storage example
sql_storage = SQLStorage(docx_extractor, './output/SQL_DB_DOCX.db')
sql_storage.save()
sql_storage.close()


# iii. For Ppt
ppt_loader = PPTLoader()
ppt_loader.file_path = 'Samples/Sample_file.pptx'  # PDF file path
ppt_extractor = PPTDataExtractor(ppt_loader)

# File storage example
file_storage = FileStorage(ppt_extractor, './output/ppt_files')
file_storage.save()

# SQL storage example
sql_storage = SQLStorage(ppt_extractor, './output/SQL_DB_PPT.db')
sql_storage.save()
sql_storage.close()
