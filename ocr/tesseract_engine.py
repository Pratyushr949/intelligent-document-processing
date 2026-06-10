import logging
from io import BytesIO
from typing import Any, Dict, List
from PIL import Image
import fitz  # PyMuPDF
import pytesseract

logger = logging.getLogger("ocr.tesseract_engine")


class TesseractEngine:
    """
    Handles scanned PDF parsing by rendering each PDF page into a high-DPI image
    and processing the resulting image through Tesseract OCR (pytesseract).
    """

    def ocr_pages(self, file_path: str, dpi: int = 150) -> List[Dict[str, Any]]:
        """
        Renders a PDF file page-by-page into images and performs OCR text extraction.

        Args:
            file_path (str): The absolute path to the scanned PDF document.
            dpi (int): Dots-per-inch resolution for rendering page pixmaps. Defaults to 150.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing page details.
                Each dictionary contains:
                - "page_number" (int): The 1-based page index.
                - "text" (str): The Tesseract OCR extracted text string.
                - "method" (str): The extraction method, set to "ocr".
        """
        logger.info(f"Starting Tesseract OCR engine extraction for: {file_path}")
        pages = []

        try:
            doc = fitz.open(file_path)
            # Convert DPI to scale factors (72 points per inch is the PDF default scale)
            scale = dpi / 72.0
            matrix = fitz.Matrix(scale, scale)

            for index, page in enumerate(doc):
                page_num = index + 1
                logger.info(f"Performing OCR on page {page_num}/{len(doc)}")

                # Render page to high-quality PNG pixmap
                pix = page.get_pixmap(matrix=matrix, alpha=False)
                img_bytes = pix.tobytes("png")

                # Load image bytes into PIL Image for Tesseract
                image = Image.open(BytesIO(img_bytes))

                # Extract text using pytesseract
                text = pytesseract.image_to_string(image) or ""

                pages.append({
                    "page_number": page_num,
                    "text": text,
                    "method": "ocr"
                })

            doc.close()
            logger.info("Successfully finished Tesseract OCR extraction on all pages.")
        except Exception as e:
            logger.error(f"Error performing OCR extraction on file {file_path}: {e}")
            raise RuntimeError(f"Failed to perform Tesseract OCR: {str(e)}") from e

        return pages
