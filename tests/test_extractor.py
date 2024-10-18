import pytest
import sys
from pathlib import Path
import psutil
import os

# Add the parent directory to sys.path for module discovery
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import your modules
from Loaders.docx_loader import DOCXLoader
from Loaders.pdf_loader import PDFLoader
from Loaders.ppt_loader import PPTLoader
from Storage.SQL_storage import MySQLStorage
@pytest.fixture
def docx_loader():
    return DOCXLoader()

@pytest.fixture
def pdf_loader():
    return PDFLoader()

@pytest.fixture
def ppt_loader():
    return PPTLoader()

# PDF Extractor Tests
def test_extract_text_from_pdf_with_text_only(pdf_loader):
    text_only_pdf_path = Path(__file__).resolve().parents[1] / "Samples/Sample_file.pdf"
    assert pdf_loader.load_file(str(text_only_pdf_path)), f"Loaded PDF with text only: {text_only_pdf_path}"

def test_extract_images_from_pdf(pdf_loader):
    images_pdf_path = Path(__file__).resolve().parents[1] / "Samples/Sample_file.pdf"
    assert pdf_loader.load_file(str(images_pdf_path)), f"Extracted images from PDF: {images_pdf_path}"

def test_extract_tables_from_pdf(pdf_loader):
    tables_pdf_path = Path(__file__).resolve().parents[1] / "Samples/Sample_file.pdf"
    assert pdf_loader.load_file(str(tables_pdf_path)), f"Extracted tables from PDF: {tables_pdf_path}"

def test_extract_urls_from_pdf(pdf_loader):
    urls_pdf_path = Path(__file__).resolve().parents[1] / "Samples/Sample_file.pdf"
    assert pdf_loader.load_file(str(urls_pdf_path)), f"Extracted URLs from PDF: {urls_pdf_path}"

def test_extract_text_and_images_from_pdf(pdf_loader):
    text_and_images_pdf_path = Path(__file__).resolve().parents[1] / "Samples/Sample_file.pdf"
    assert pdf_loader.load_file(str(text_and_images_pdf_path)), f"Extracted text and images from PDF: {text_and_images_pdf_path}"

def test_extract_all_content_from_large_pdf(pdf_loader):
    large_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(str(large_pdf_path)), f"Extracted all content from large PDF: {large_pdf_path}"

def test_extract_text_with_special_characters_from_pdf(pdf_loader):
    special_chars_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/special_characters.pdf"
    assert pdf_loader.load_file(str(special_chars_pdf_path)), f"Extracted text with special characters from PDF: {special_chars_pdf_path}"

def test_handle_empty_pdf(pdf_loader):
    empty_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/empty.pdf"
    assert not pdf_loader.load_file(str(empty_pdf_path)), f"Handled empty PDF file: {empty_pdf_path}"

def test_handle_corrupted_pdf(pdf_loader):
    corrupted_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/corrupt.pdf"
    
    # Attempt to load the corrupted PDF and check if the returned value is an error message.
    result = pdf_loader.load_file(str(corrupted_pdf_path))

    # Assert that the result contains the error message as the method does not raise an exception.
    assert "Error loading PDF:" in result, f"Expected error message, but got: {result}"



def test_handle_password_protected_pdf(pdf_loader):
    password_protected_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/password.pdf"
    assert not pdf_loader.load_file(str(password_protected_pdf_path)), f"Handled password protected PDF file: {password_protected_pdf_path}"

def test_handle_pdf_with_missing_embedded_fonts(pdf_loader):
    missing_fonts_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/missing_fonts.pdf"
    assert not pdf_loader.load_file(str(missing_fonts_pdf_path)), f"Handled PDF with missing embedded fonts: {missing_fonts_pdf_path}"

def test_extract_text_from_scanned_pdf(pdf_loader):
    scanned_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/scanned.pdf"
    assert pdf_loader.load_file(str(scanned_pdf_path)), f"Extracted text from scanned PDF: {scanned_pdf_path}"

def test_extract_hyperlinks_and_anchors_from_pdf(pdf_loader):
    hyperlinks_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/hyperlinks.pdf"
    assert pdf_loader.load_file(str(hyperlinks_pdf_path)), f"Extracted hyperlinks and anchors from PDF: {hyperlinks_pdf_path}"

def test_extract_form_fields_from_interactive_pdf(pdf_loader):
    interactive_pdf_path = Path(__file__).resolve().parents[1] / "test_files/pdf/interactive.pdf"
    assert pdf_loader.load_file(str(interactive_pdf_path)), f"Extracted form fields from interactive PDF: {interactive_pdf_path}"

# DOCX Extractor Tests
def test_extract_text_from_docx_with_text_only(docx_loader):
    text_only_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/text_only.docx"
    assert docx_loader.load_file(str(text_only_docx_path)), f"Loaded DOCX with text only: {text_only_docx_path}"

def test_extract_images_from_docx(docx_loader):
    images_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/images.docx"
    assert docx_loader.load_file(str(images_docx_path)), f"Extracted images from DOCX: {images_docx_path}"

def test_extract_tables_from_docx(docx_loader):
    tables_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/tables.docx"
    assert docx_loader.load_file(str(tables_docx_path)), f"Extracted tables from DOCX: {tables_docx_path}"

def test_extract_urls_from_docx(docx_loader):
    urls_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/urls.docx"
    assert docx_loader.load_file(str(urls_docx_path)), f"Extracted URLs from DOCX: {urls_docx_path}"

def test_extract_text_from_multi_page_docx(docx_loader):
    multi_page_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/multi_page.docx"
    assert docx_loader.load_file(str(multi_page_docx_path)), f"Extracted text from multi-page DOCX: {multi_page_docx_path}"

def test_extract_text_with_special_characters_from_docx(docx_loader):
    special_chars_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/special_characters.docx"
    assert docx_loader.load_file(str(special_chars_docx_path)), f"Extracted text with special characters from DOCX: {special_chars_docx_path}"

def test_extract_footnotes_and_endnotes_from_docx(docx_loader):
    footnotes_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/footnotes.docx"
    assert docx_loader.load_file(str(footnotes_docx_path)), f"Extracted footnotes and endnotes from DOCX: {footnotes_docx_path}"

def test_extract_text_considering_section_breaks(docx_loader):
    section_breaks_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/section_breaks.docx"
    assert docx_loader.load_file(str(section_breaks_docx_path)), f"Extracted text considering section breaks from DOCX: {section_breaks_docx_path}"

def test_extract_headers_and_footers_from_docx(docx_loader):
    headers_footers_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/headers_footers.docx"
    assert docx_loader.load_file(str(headers_footers_docx_path)), f"Extracted headers and footers from DOCX: {headers_footers_docx_path}"

def test_extract_comments_from_docx(docx_loader):
    comments_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/comments.docx"
    assert docx_loader.load_file(str(comments_docx_path)), f"Extracted comments from DOCX: {comments_docx_path}"

def test_extract_tracked_changes_from_docx(docx_loader):
    tracked_changes_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/tracked_changes.docx"
    assert docx_loader.load_file(str(tracked_changes_docx_path)), f"Extracted tracked changes from DOCX: {tracked_changes_docx_path}"

def test_extract_content_from_large_docx(docx_loader):
    large_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/large.docx"
    assert docx_loader.load_file(str(large_docx_path)), f"Extracted content from large DOCX: {large_docx_path}"

def test_handle_corrupted_docx(docx_loader):
    corrupted_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/corrupted.docx"
    assert not docx_loader.load_file(str(corrupted_docx_path)), f"Handled corrupted DOCX file: {corrupted_docx_path}"

def test_handle_encrypted_docx(docx_loader):
    encrypted_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/encrypted.docx"
    assert not docx_loader.load_file(str(encrypted_docx_path)), f"Handled encrypted DOCX file: {encrypted_docx_path}"

def test_extract_tables_with_merged_cells_from_docx(docx_loader):
    merged_cells_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/merged_cells.docx"
    assert docx_loader.load_file(str(merged_cells_docx_path)), f"Extracted tables with merged cells from DOCX: {merged_cells_docx_path}"

def test_extract_hyperlinks_from_docx(docx_loader):
    hyperlinks_docx_path = Path(__file__).resolve().parents[1] / "test_files/docx/hyperlinks.docx"
    assert docx_loader.load_file(str(hyperlinks_docx_path)), f"Extracted hyperlinks from DOCX: {hyperlinks_docx_path}"

# PPTX Extractor Tests
def test_extract_text_from_pptx_with_text_only(ppt_loader):
    text_only_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/text_only.pptx"
    assert ppt_loader.load_file(str(text_only_pptx_path)), f"Loaded PPTX with text only: {text_only_pptx_path}"

def test_extract_images_from_pptx(ppt_loader):
    images_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/images.pptx"
    assert ppt_loader.load_file(str(images_pptx_path)), f"Extracted images from PPTX: {images_pptx_path}"

def test_extract_tables_from_pptx(ppt_loader):
    tables_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/tables.pptx"
    assert ppt_loader.load_file(str(tables_pptx_path)), f"Extracted tables from PPTX: {tables_pptx_path}"

def test_extract_urls_from_pptx(ppt_loader):
    urls_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/urls.pptx"
    assert ppt_loader.load_file(str(urls_pptx_path)), f"Extracted URLs from PPTX: {urls_pptx_path}"

def test_handle_pptx_slides_with_animations(ppt_loader):
    animations_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/animations.pptx"
    assert ppt_loader.load_file(str(animations_pptx_path)), f"Handled PPTX slides with animations: {animations_pptx_path}"

def test_extract_embedded_objects_from_pptx(ppt_loader):
    embedded_objects_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/embedded_objects.pptx"
    assert ppt_loader.load_file(str(embedded_objects_pptx_path)), f"Extracted embedded objects from PPTX: {embedded_objects_pptx_path}"

def test_extract_content_considering_master_slides(ppt_loader):
    master_slides_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/master_slides.pptx"
    assert ppt_loader.load_file(str(master_slides_pptx_path)), f"Extracted content considering master slides from PPTX: {master_slides_pptx_path}"

def test_extract_hyperlinks_from_pptx(ppt_loader):
    hyperlinks_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/hyperlinks.pptx"
    assert ppt_loader.load_file(str(hyperlinks_pptx_path)), f"Extracted hyperlinks from PPTX: {hyperlinks_pptx_path}"

def test_extract_notes_from_notes_section_of_pptx(ppt_loader):
    notes_section_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/notes_section.pptx"
    assert ppt_loader.load_file(str(notes_section_pptx_path)), f"Extracted notes from notes section of PPTX: {notes_section_pptx_path}"

def test_extract_all_content_from_large_pptx(ppt_loader):
    large_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/large.pptx"
    assert ppt_loader.load_file(str(large_pptx_path)), f"Extracted all content from large PPTX: {large_pptx_path}"

def test_handle_corrupted_pptx(ppt_loader):
    corrupted_pptx_path = Path(__file__).resolve().parents[1] / "test_files/pptx/corrupted.pptx"
    assert not ppt_loader.load_file(str(corrupted_pptx_path)), f"Handled corrupted PPTX file: {corrupted_pptx_path}"


# Mixed Content Types and Performance Tests
def test_handle_empty_file_extraction(file_loader):
    empty_file_path = Path(__file__).resolve().parents[1] / "test_files/empty_file"
    assert not file_loader.load_file(str(empty_file_path)), f"Handled empty file extraction: {empty_file_path}"

def test_handle_extraction_from_file_with_mixed_content_types(file_loader):
    mixed_content_file_path = Path(__file__).resolve().parents[1] / "test_files/mixed_content"
    assert file_loader.load_file(str(mixed_content_file_path)), f"Handled extraction from mixed content types: {mixed_content_file_path}"

def test_handle_unsupported_file_format(file_loader):
    unsupported_file_path = Path(__file__).resolve().parents[1] / "test_files/unsupported.txt"
    assert not file_loader.load_file(str(unsupported_file_path)), f"Handled unsupported file format: {unsupported_file_path}"

def test_handle_extraction_from_very_large_files(file_loader):
    very_large_file_path = Path(__file__).resolve().parents[1] / "test_files/very_large_file.pdf"
    assert file_loader.load_file(str(very_large_file_path)), f"Handled extraction from a very large file: {very_large_file_path}"

def test_handle_files_with_corrupted_metadata(file_loader):
    corrupted_metadata_file_path = Path(__file__).resolve().parents[1] / "test_files/corrupted_metadata.pdf"
    assert not file_loader.load_file(str(corrupted_metadata_file_path)), f"Handled files with corrupted metadata: {corrupted_metadata_file_path}"


# Performance Tests
def test_extraction_time_for_very_large_files(file_loader):
    very_large_file_path = Path(__file__).resolve().parents[1] / "test_files/very_large_file.pdf"
    import time
    start_time = time.time()
    file_loader.load_file(str(very_large_file_path))
    elapsed_time = time.time() - start_time
    assert elapsed_time < 60, f"Extraction time for very large files exceeded: {elapsed_time}s"

def test_extraction_for_multiple_files_concurrently(file_loader):
    file_paths = [Path(__file__).resolve().parents[1] / f"test_files/multiple_file_{i}.pdf" for i in range(5)]
    results = [file_loader.load_file(str(file_path)) for file_path in file_paths]
    assert all(results), "Failed to extract from multiple files concurrently."

def test_stress_test_with_large_number_of_files(file_loader):
    file_paths = [Path(__file__).resolve().parents[1] / f"test_files/stress_test_file_{i}.pdf" for i in range(100)]
    results = [file_loader.load_file(str(file_path)) for file_path in file_paths]
    assert all(results), "Failed to extract from a large number of files."

def test_measure_memory_usage_for_large_files(file_loader):
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    very_large_file_path = Path(__file__).resolve().parents[1] / "test_files/very_large_file.pdf"
    file_loader.load_file(str(very_large_file_path))
    memory_after = process.memory_info().rss
    assert memory_after - memory_before < 500 * 1024 * 1024, "Memory usage exceeded 500MB for large file extraction."

def test_extract_content_from_compressed_files(file_loader):
    compressed_file_path = Path(__file__).resolve().parents[1] / "test_files/compressed_files.zip"
    assert file_loader.load_file(str(compressed_file_path)), f"Extracted content from compressed files: {compressed_file_path}"

# Security Tests
def test_attempt_to_extract_content_from_unsupported_file_format(file_loader):
    unsupported_file_path = Path(__file__).resolve().parents[1] / "test_files/unsupported_format.doc"
    assert not file_loader.load_file(str(unsupported_file_path)), f"Handled extraction attempt from unsupported file format: {unsupported_file_path}"

def test_extract_content_from_file_with_corrupted_sections(file_loader):
    corrupted_sections_file_path = Path(__file__).resolve().parents[1] / "test_files/corrupted_sections.pdf"
    assert not file_loader.load_file(str(corrupted_sections_file_path)), f"Handled extraction from a file with corrupted sections: {corrupted_sections_file_path}"

def test_extraction_with_read_only_permissions_on_files(file_loader):
    read_only_file_path = Path(__file__).resolve().parents[1] / "test_files/read_only.pdf"
    assert not file_loader.load_file(str(read_only_file_path)), f"Handled extraction with read-only permissions on file: {read_only_file_path}"

def test_extraction_without_necessary_software_libraries(file_loader):
    # Mock or simulate absence of libraries
    assert not file_loader.load_file("dummy_path"), "Handled extraction without necessary software libraries."

def test_handle_incomplete_or_partially_downloaded_files(file_loader):
    incomplete_file_path = Path(__file__).resolve().parents[1] / "test_files/incomplete_downloaded.pdf"
    assert not file_loader.load_file(str(incomplete_file_path)), f"Handled incomplete or partially downloaded file: {incomplete_file_path}"


# Language and Internationalization Tests
def test_handle_files_with_non_english_languages(file_loader):
    non_english_file_path = Path(__file__).resolve().parents[1] / "test_files/non_english_file.pdf"
    assert file_loader.load_file(str(non_english_file_path)), f"Handled files with non-English languages: {non_english_file_path}"

def test_extract_content_from_files_containing_multiple_languages(file_loader):
    multi_language_file_path = Path(__file__).resolve().parents[1] / "test_files/multi_language_file.pdf"
    assert file_loader.load_file(str(multi_language_file_path)), f"Extracted content from files containing multiple languages: {multi_language_file_path}"

def test_handle_language_specific_formatting(file_loader):
    arabic_file_path = Path(__file__).resolve().parents[1] / "test_files/arabic_language_file.pdf"
    assert file_loader.load_file(str(arabic_file_path)), f"Handled language-specific formatting for Arabic: {arabic_file_path}"

def test_display_error_messages_in_user_locale(file_loader):
    error_file_path = Path(__file__).resolve().parents[1] / "test_files/error_message_file.pdf"
    assert not file_loader.load_file(str(error_file_path)), f"Displayed error messages in user’s locale/language for: {error_file_path}"

def test_handle_special_characters_and_symbols(file_loader):
    special_characters_file_path = Path(__file__).resolve().parents[1] / "test_files/special_characters_file.pdf"
    assert file_loader.load_file(str(special_characters_file_path)), f"Handled special characters and symbols for different languages: {special_characters_file_path}"


# Additional Extraction Tests
def test_extract_files_with_embedded_audio_or_media(file_loader):
    audio_media_file_path = Path(__file__).resolve().parents[1] / "test_files/embedded_audio.pptx"
    assert file_loader.load_file(str(audio_media_file_path)), f"Extracted files with embedded audio or media: {audio_media_file_path}"

def test_extract_files_with_embedded_video_content(file_loader):
    video_content_file_path = Path(__file__).resolve().parents[1] / "test_files/embedded_video.pptx"
    assert file_loader.load_file(str(video_content_file_path)), f"Extracted files with embedded video content: {video_content_file_path}"

def test_handle_files_containing_interactive_content(file_loader):
    interactive_file_path = Path(__file__).resolve().parents[1] / "test_files/interactive_content.pdf"
    assert file_loader.load_file(str(interactive_file_path)), f"Handled files containing interactive content: {interactive_file_path}"

def test_handle_files_containing_3d_models_or_specialized_embedded_objects(file_loader):
    embedded_objects_file_path = Path(__file__).resolve().parents[1] / "test_files/embedded_3d_models.pptx"
    assert file_loader.load_file(str(embedded_objects_file_path)), f"Handled files containing 3D models or specialized embedded objects: {embedded_objects_file_path}"

def test_extract_content_from_files_with_watermarks(file_loader):
    watermark_file_path = Path(__file__).resolve().parents[1] / "test_files/watermarked_file.pdf"
    assert file_loader.load_file(str(watermark_file_path)), f"Extracted content from files with watermarks: {watermark_file_path}"

# test_extractor.py

# Assuming extract_content is defined in another module (e.g., 'extractor.py')
# Import the function from the correct module
from tests.extractor import extract_content  # Adjust the module name as needed

# Test cases for the extract_content function
def test_extract_content_with_valid_file():
    # Assuming you are testing extraction from a valid file
    file_path = "Samples/Sample_file.pptx"  # Example file path
    result = extract_content(file_path)
    
    # Assert conditions to check the correct extraction
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "text" in result, "Extracted content should include text"
    assert "images" in result, "Extracted content should include images"
    assert "links" in result, "Extracted content should include links"
    assert "tables" in result, "Extracted content should include tables"

def test_extract_content_with_invalid_file():
    # Test with an invalid file or unsupported format
    file_path = "invalid_file.xyz"  # Example invalid file path
    try:
        extract_content(file_path)
        assert False, "Exception should have been raised for invalid file"
    except Exception as e:
        assert isinstance(e, ValueError), "Should raise a ValueError for invalid file type"

def test_extract_content_with_empty_file():
    # Test with an empty file
    file_path = "test_files/pptx/empty.pptx"  # Example empty file path
    result = extract_content(file_path)
    
    # Check for expected behavior (e.g., empty content)
    assert isinstance(result, dict), "Result should be a dictionary"
    assert not result["text"], "Text content should be empty"
    assert not result["images"], "Image content should be empty"
    assert not result["links"], "Link content should be empty"
    assert not result["tables"], "Table content should be empty"

# Additional test cases can be added as needed


# import pytest
# from  tests.test_extractor import extract_content  # Adjust based on your actual import

# def test_handle_corrupted_pdf():
#     with pytest.raises(ValueError, match="Cannot extract content from corrupted PDF"):
#         extract_content('/home/shtlp_0108/Desktop/Assignment3-Python/test_files/pdf/corrupted.pdf')

# def test_handle_password_protected_pdf():
#     with pytest.raises(ValueError, match="Cannot extract content from password-protected PDF"):
#         extract_content('/home/shtlp_0108/Desktop/Assignment3-Python/test_files/pdf/password_protected.pdf')

# def test_handle_pdf_with_missing_embedded_fonts():
#     with pytest.raises(ValueError, match="PDF has missing embedded fonts"):
#         extract_content('/home/shtlp_0108/Desktop/Assignment3-Python/test_files/pdf/missing_fonts.pdf')

# def test_handle_corrupted_docx():
#     with pytest.raises(ValueError, match="Cannot extract content from corrupted DOCX"):
#         extract_content('/home/shtlp_0108/Desktop/Assignment3-Python/test_files/docx/corrupted.docx')

# def test_handle_encrypted_docx():
#     with pytest.raises(ValueError, match="Cannot extract content from encrypted DOCX"):
#         extract_content('/home/shtlp_0108/Desktop/Assignment3-Python/test_files/docx/encrypted.docx')

# def test_handle_corrupted_pptx():
#     with pytest.raises(ValueError, match="Cannot extract content from corrupted PPTX"):
#         extract_content('/home/shtlp_0108/Desktop/Assignment3-Python/test_files/pptx/corrupted.pptx')

# # Add similar modifications for other test cases based on their specific requirements

# # def extract_content(file_path):
# #     # Logic to handle file extraction
# #     if is_corrupted(file_path):
# #         raise ValueError("Cannot extract content from corrupted PDF")
# #     if is_password_protected(file_path):
# #         raise ValueError("Cannot extract content from password-protected PDF")
# #     if has_missing_embedded_fonts(file_path):
# #         raise ValueError("PDF has missing embedded fonts")
# #     # Continue for other checks

