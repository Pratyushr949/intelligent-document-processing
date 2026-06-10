import logging
import re
from typing import Any, Dict

logger = logging.getLogger("classify.validator")

# Verhoeff tables
VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]


class Validator:
    """
    Validates structural correctness of extracted entities like Email, Phone,
    PAN, Aadhaar, Vehicle Registration Number, and IFSC Codes.
    """

    def validate(self, value: str, type_label: str) -> Dict[str, Any]:
        """
        Orchestrates validation based on the target type_label.

        Args:
            value (str): Text value to validate.
            type_label (str): Entity class (Email, Aadhaar, IFSC, etc.)

        Returns:
            Dict[str, Any]: Verification summary conforming to:
                {
                    "valid": bool,
                    "errors": List[str]
                }
        """
        val = str(value).strip()
        label = type_label.strip()

        if label == "Email":
            return self.validate_email(val)
        elif label == "Phone":
            return self.validate_phone(val)
        elif label == "PAN":
            return self.validate_pan(val)
        elif label == "Aadhaar":
            return self.validate_aadhaar(val)
        elif label == "Vehicle Number":
            return self.validate_vehicle_number(val)
        elif label == "IFSC":
            return self.validate_ifsc(val)
        else:
            return {
                "valid": False,
                "errors": [f"Validation is not supported for type '{type_label}'."]
            }

    def validate_email(self, value: str) -> Dict[str, Any]:
        email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if email_regex.match(value):
            return {"valid": True, "errors": []}
        return {"valid": False, "errors": ["Invalid email formatting structure."]}

    def validate_phone(self, value: str) -> Dict[str, Any]:
        # Strip standard separators
        cleaned = re.sub(r'[\s\-()+\.]', '', value)
        if cleaned.isdigit() and 10 <= len(cleaned) <= 15:
            return {"valid": True, "errors": []}
        return {"valid": False, "errors": ["Phone number must contain between 10 and 15 digits."]}

    def validate_pan(self, value: str) -> Dict[str, Any]:
        pan_regex = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
        if pan_regex.match(value.upper()):
            return {"valid": True, "errors": []}
        return {"valid": False, "errors": ["PAN number must be 10 characters formatted as: 5 letters, 4 digits, 1 letter."]}

    def validate_aadhaar(self, value: str) -> Dict[str, Any]:
        cleaned = re.sub(r'[\s\-]', '', value)
        if len(cleaned) != 12 or not cleaned.isdigit():
            return {"valid": False, "errors": ["Aadhaar number must contain exactly 12 numeric digits."]}

        if cleaned[0] in ('0', '1'):
            return {"valid": False, "errors": ["Aadhaar number cannot start with digit 0 or 1."]}

        # Perform Verhoeff checksum algorithm calculation
        digits = [int(char) for char in cleaned]
        checksum = 0
        for i, val in enumerate(reversed(digits)):
            checksum = VERHOEFF_D[checksum][VERHOEFF_P[i % 8][val]]

        if checksum == 0:
            return {"valid": True, "errors": []}
        return {"valid": False, "errors": ["Invalid Aadhaar Verhoeff checksum signature."]}

    def validate_vehicle_number(self, value: str) -> Dict[str, Any]:
        cleaned = re.sub(r'[\s\-]', '', value).upper()
        # Pattern match for Indian Vehicle registrations: STATE-DISTRICT-SERIES-NUMBER
        vehicle_regex = re.compile(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$')
        if vehicle_regex.match(cleaned):
            return {"valid": True, "errors": []}
        return {"valid": False, "errors": ["Invalid vehicle registration format structure."]}

    def validate_ifsc(self, value: str) -> Dict[str, Any]:
        cleaned = value.replace(" ", "").upper()
        ifsc_regex = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')
        if ifsc_regex.match(cleaned):
            return {"valid": True, "errors": []}
        return {"valid": False, "errors": ["IFSC code must be 11 characters formatted as: 4 letters, 0, 6 alpha-numeric characters."]}
