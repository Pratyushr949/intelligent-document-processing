import logging
from typing import Any, Dict, List
import fitz  # PyMuPDF

logger = logging.getLogger("ocr.pdf_reader")


class PDFReader:
    """
    Handles digital text extraction from PDF documents using PyMuPDF (fitz)
    and determines whether OCR is necessary based on content density.
    """

    def read_digital_pages(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extracts native text from a digital PDF file page-by-page.

        Args:
            file_path (str): The absolute path to the PDF file.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing page details.
                Each dictionary contains:
                - "page_number" (int): The 1-based page index.
                - "text" (str): The raw extracted text string.
                - "method" (str): The extraction method, default is "digital".
        """
        logger.info(f"Extracting native digital text from file: {file_path}")
        pages = []

        try:
            doc = fitz.open(file_path)
            for index, page in enumerate(doc):
                text = page.get_text() or ""
                pages.append({
                    "page_number": index + 1,
                    "text": text,
                    "method": "digital"
                })
            doc.close()
            logger.debug(f"Successfully extracted {len(pages)} pages digitally.")
        except Exception as e:
            logger.error(f"Error reading digital PDF pages from {file_path}: {e}")
            raise RuntimeError(f"Failed to read PDF digitally: {str(e)}") from e

        return pages

    def needs_ocr(self, pages: List[Dict[str, Any]], threshold: int = 50) -> bool:
        """
        Determines if the document requires OCR extraction by verifying if the
        total text length is less than the character count threshold.

        Args:
            pages (List[Dict[str, Any]]): Extracted pages from read_digital_pages.
            threshold (int): Character count threshold to trigger OCR. Defaults to 50.

        Returns:
            bool: True if OCR is required, False if the digital text is sufficient.
        """
        total_chars = sum(len(page.get("text", "").strip()) for page in pages)
        logger.info(f"Digital text detection: total characters found = {total_chars}")

        # Trigger OCR if the document contains very sparse or no digital text
        if total_chars < threshold:
            logger.info(f"Document contains insufficient digital text (< {threshold} chars). OCR is required.")
            return True

        logger.info(f"Document contains sufficient digital text. Skipping OCR step.")
        return False
