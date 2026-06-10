import json
import logging
import re
from typing import Dict

import yaml
from google.genai import Client

from agents.base import BaseDocumentAgent
from config.config_loader import settings

logger = logging.getLogger("classify.pii_detector")


class PIIDetector(BaseDocumentAgent):

    def __init__(self, **kwargs):

        prompts_path = (
            settings.base_dir
            / "config"
            / "pii_detection_prompts.yaml"
        )

        system_instruction = ""
        user_prompt_template = ""

        if prompts_path.exists():
            try:
                with open(prompts_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}

                pii_config = config.get(
                    "pii_detection",
                    {}
                )

                system_instruction = pii_config.get(
                    "system_instruction",
                    ""
                )

                user_prompt_template = pii_config.get(
                    "user_prompt_template",
                    ""
                )

            except Exception as e:
                logger.error(
                    f"Failed loading PII prompts: {e}"
                )

        super().__init__(
            name="pii_detector",
            instruction=system_instruction,
            **kwargs
        )

        object.__setattr__(
            self,
            "user_prompt_template",
            user_prompt_template
        )

        object.__setattr__(
            self,
            "client",
            Client(api_key=settings.gemini_api_key)
        )

    def process_document(
        self,
        file_path: str,
        **kwargs
    ) -> Dict:
        return {
            "agent": self.name,
            "status": "active"
        }

    def detect_pii(
        self,
        text: str
    ) -> Dict:

        if not text or not text.strip():
            return {
                "pii_entities": []
            }

        prompt_template = getattr(
            self,
            "user_prompt_template",
            ""
        )

        if prompt_template:
            prompt = prompt_template.format(
                text=text[:15000]
            )
        else:
            prompt = (
                "Detect PII in the following text:\n\n"
                f"{text[:15000]}"
            )

        try:

            logger.info(
                "Executing Gemini PII detection..."
            )

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            response_text = response.text

            logger.info(
                "Gemini PII detection completed."
            )

            return self._parse_json_response(
                response_text
            )

        except Exception as e:

            logger.error(
                f"PII detection failed: {e}"
            )

            return {
                "pii_entities": [],
                "error": str(e)
            }

    def _parse_json_response(
        self,
        text: str
    ) -> Dict:

        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(
                r"^```(?:json)?\n?",
                "",
                cleaned,
                flags=re.IGNORECASE
            )

            cleaned = re.sub(
                r"\n?```$",
                "",
                cleaned
            ).strip()

        try:

            parsed = json.loads(cleaned)

            if isinstance(parsed, dict):
                return parsed

            if isinstance(parsed, list):
                return {
                    "pii_entities": parsed
                }

            return {
                "pii_entities": []
            }

        except Exception:

            return {
                "pii_entities": [],
                "raw_response": cleaned
            }