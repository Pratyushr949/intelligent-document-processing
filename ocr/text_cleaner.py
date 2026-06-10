import logging
import re
import unicodedata

logger = logging.getLogger("ocr.text_cleaner")


class TextCleaner:
    """
    Utility module for cleaning, formatting, and normalizing text extracted
    from digital PDF reading or OCR.
    """

    def clean_text(self, text: str) -> str:
        """
        Applies cleaning rules to raw text:
        1. Normalizes Unicode characters to NFKC form.
        2. Normalizes non-newline whitespace (tabs, horizontal spaces).
        3. Collapses multiple vertical spacing/newlines into double newlines.
        4. Strips leading and trailing whitespaces.

        Args:
            text (str): Raw input text to be cleaned.

        Returns:
            str: Normalized and sanitized output text.
        """
        if not text:
            return ""

        # Normalize unicode format (collapsing ligatures and accents)
        cleaned = unicodedata.normalize("NFKC", text)

        # Normalize line-level spacing (collapsing consecutive tabs/spaces into single spaces)
        cleaned = re.sub(r"[ \t\r\f\v]+", " ", cleaned)

        # Collapse excess empty lines (limiting consecutive line breaks to a max of two)
        cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned)

        # Remove leading/trailing document whitespaces
        cleaned = cleaned.strip()

        logger.debug("Successfully cleaned text stream.")
        return cleaned
