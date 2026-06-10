import json
import logging
import re
from typing import Dict

import yaml
from google.genai import Client

from agents.base import BaseDocumentAgent
from config.config_loader import settings

logger = logging.getLogger("classify.llm_classifier")


class LLMDocumentClassifier(BaseDocumentAgent):
    """
    LLM-based document classifier using Gemini SDK.
    """

    def __init__(self, **kwargs):

        prompts_path = (
            settings.base_dir
            / "config"
            / "classification_prompts.yaml"
        )

        system_instruction = ""
        user_prompt_template = ""

        if prompts_path.exists():
            try:
                with open(prompts_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}

                class_config = config.get(
                    "document_classification",
                    {}
                )

                system_instruction = class_config.get(
                    "system_instruction",
                    ""
                )

                user_prompt_template = class_config.get(
                    "user_prompt_template",
                    ""
                )

            except Exception as e:
                logger.error(
                    f"Failed to load classification prompts: {e}"
                )

        super().__init__(
            name="llm_classifier",
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

    def classify_text(
        self,
        text: str
    ) -> Dict:

        if not text or not text.strip():
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "reasoning": "Empty document text."
            }

        capped_text = text[:15000]

        prompt_template = getattr(
            self,
            "user_prompt_template",
            ""
        )

        if prompt_template:
            user_prompt = prompt_template.format(
                text=capped_text
            )
        else:
            user_prompt = (
                "Classify the following document:\n\n"
                f"{capped_text}"
            )

        try:

            logger.info(
                "Executing Gemini classification request..."
            )

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt
            )

            response_text = response.text

            logger.info(
                "Gemini classification completed successfully."
            )

            return self._parse_json_response(
                response_text
            )

        except Exception as e:

            logger.error(
                f"Classification failed: {e}"
            )

            return {
                "category": "Unknown",
                "confidence": 0.0,
                "reasoning": str(e)
            }

    def _parse_json_response(
        self,
        text: str
    ) -> Dict:

        cleaned_text = text.strip()

        if cleaned_text.startswith("```"):
            cleaned_text = re.sub(
                r"^```(?:json)?\n?",
                "",
                cleaned_text,
                flags=re.IGNORECASE
            )

            cleaned_text = re.sub(
                r"\n?```$",
                "",
                cleaned_text
            ).strip()

        try:

            parsed = json.loads(
                cleaned_text
            )

            return {
                "category": parsed.get(
                    "category",
                    "Unknown"
                ),
                "confidence": float(
                    parsed.get(
                        "confidence",
                        0.0
                    )
                ),
                "reasoning": parsed.get(
                    "reasoning",
                    ""
                )
            }

        except Exception:

            return {
                "category": "Unknown",
                "confidence": 0.0,
                "reasoning": cleaned_text
            }