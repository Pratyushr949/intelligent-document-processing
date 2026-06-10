import logging
from pathlib import Path
from typing import Any, Dict
from ocr.pdf_reader import PDFReader
from ocr.tesseract_engine import TesseractEngine
from ocr.text_cleaner import TextCleaner

logger = logging.getLogger("ocr.service")


class OCRService:
    """
    Service responsible for orchestrating document text extraction.
    Automatically detects if digital PDF extraction is possible, 
    otherwise falls back to Tesseract OCR, cleaning all outputs.
    """

    def __init__(self):
        self.pdf_reader = PDFReader()
        self.ocr_engine = TesseractEngine()
        self.cleaner = TextCleaner()
        logger.info("OCR Service initialized with PyMuPDF, Tesseract, and Cleaner utilities.")

    def run_ocr(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Reads a document, automatically performs OCR if required, 
        cleans the resulting text, and returns the structured output.
        
        Args:
            file_path (str): The absolute path to the PDF file.

        Returns:
            Dict[str, Any]: Formatted dictionary according to the schema:
                {
                    "document_id": str,
                    "pages": List[Dict[str, Any]],
                    "raw_text": str
                }
        """
        logger.info(f"Initiating OCR service task for document: {file_path}")
        document_id = Path(file_path).stem

        try:
            # 1. Read digital PDF first
            pages = self.pdf_reader.read_digital_pages(file_path)

            # 2. Automatically detect if OCR is required
            if self.pdf_reader.needs_ocr(pages):
                logger.info("Digital text missing or sparse. Running Tesseract OCR engine...")
                pages = self.ocr_engine.ocr_pages(file_path)

            # 3. Clean page text and compile raw text
            cleaned_pages = []
            raw_text_segments = []

            for page in pages:
                cleaned_page_text = self.cleaner.clean_text(page.get("text", ""))
                cleaned_pages.append({
                    "page_number": page.get("page_number"),
                    "text": cleaned_page_text,
                    "method": page.get("method")
                })
                raw_text_segments.append(cleaned_page_text)

            # Join pages using a newline character to create the unified raw_text block
            raw_text = "\n\n".join(raw_text_segments)

            logger.info(f"OCR service task completed successfully for file: {file_path}")
            return {
                "document_id": document_id,
                "pages": cleaned_pages,
                "raw_text": raw_text
            }

        except Exception as e:
            logger.error(f"Error encountered during OCR service execution for file {file_path}: {e}")
            return {
                "document_id": document_id,
                "pages": [],
                "raw_text": f"Error: {str(e)}"
            }

