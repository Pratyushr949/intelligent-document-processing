import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger("classify.rule_classifier")


class RuleClassifier:
    """
    Regex-based entity classifier that matches patterns like Email, Phone, PAN,
    Aadhaar, IFSC, Vehicle Number, and Bank Account Numbers from raw text contents.
    All successful pattern matches receive a default confidence score of 1.0.
    """

    def __init__(self):
        # Configure regex patterns
        self.email_pattern = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b')
        self.phone_pattern = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
        self.pan_pattern = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b')
        self.aadhaar_pattern = re.compile(r'\b[2-9]{1}[0-9]{3}[-\s]?[0-9]{4}[-\s]?[0-9]{4}\b')
        self.ifsc_pattern = re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b')
        self.vehicle_pattern = re.compile(r'\b[A-Z]{2}[-\s]?\d{2}[-\s]?[A-Z]{1,2}[-\s]?\d{4}\b')
        self.bank_account_pattern = re.compile(r'\b\d{9,18}\b')

    def classify_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Scans input text and returns all unique pattern matches.

        Args:
            text (str): Input document text.

        Returns:
            List[Dict[str, Any]]: List of matching results formatted as:
                {
                    "type": str,
                    "value": str,
                    "confidence": 1.0
                }
        """
        if not text:
            return []

        matches = []
        seen_values = set()

        def scan_pattern(pattern: re.Pattern, type_label: str):
            for match in pattern.finditer(text):
                value = match.group(0).strip()

                # Deduplicate to prevent duplicates
                if (type_label, value) in seen_values:
                    continue

                # To prevent Bank Account pattern from false-positive matching Aadhaar or Phone strings
                if type_label == "Bank Account Number":
                    if self.aadhaar_pattern.match(value) or self.phone_pattern.match(value):
                        continue

                seen_values.add((type_label, value))
                matches.append({
                    "type": type_label,
                    "value": value,
                    "confidence": 1.0
                })

        # Run regex scans
        scan_pattern(self.email_pattern, "Email")
        scan_pattern(self.phone_pattern, "Phone")
        scan_pattern(self.pan_pattern, "PAN")
        scan_pattern(self.aadhaar_pattern, "Aadhaar")
        scan_pattern(self.ifsc_pattern, "IFSC")
        scan_pattern(self.vehicle_pattern, "Vehicle Number")
        scan_pattern(self.bank_account_pattern, "Bank Account Number")

        logger.info(f"Rule classifier matched {len(matches)} pattern entities.")
        return matches
