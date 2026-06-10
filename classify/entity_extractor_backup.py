import json
import logging
import re
from typing import Dict
import yaml

from agents.base import BaseDocumentAgent
from config.config_loader import settings

logger = logging.getLogger("classify.entity_extractor")


class EntityExtractor(BaseDocumentAgent):

    def __init__(self, **kwargs):

        prompts_path = (
            settings.base_dir
            / "config"
            / "entity_extraction_prompts.yaml"
        )

        system_instruction = ""
        user_prompt_template = ""

        if prompts_path.exists():
            try:
                with open(prompts_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}

                entity_config = config.get(
                    "entity_extraction",
                    {}
                )

                system_instruction = entity_config.get(
                    "system_instruction",
                    ""
                )

                user_prompt_template = entity_config.get(
                    "user_prompt_template",
                    ""
                )

            except Exception as e:
                logger.error(
                    f"Failed loading entity prompts: {e}"
                )

        super().__init__(
            name="entity_extractor",
            instruction=system_instruction,
            **kwargs
        )

        object.__setattr__(
            self,
            "user_prompt_template",
            user_prompt_template
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

    def extract_entities(
        self,
        text: str
    ) -> Dict:

        if not text:
            return {"entities": []}

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
                "Extract entities from:\n\n"
                + text[:15000]
            )

        try:

            if hasattr(self, "run"):
                response = self.run(
                    prompt=prompt
                )
            else:
                response = "[]"

            if hasattr(response, "text"):
                response_text = response.text
            else:
                response_text = str(response)

            return self._parse_json_response(
                response_text
            )

        except Exception as e:

            logger.error(
                f"Entity extraction failed: {e}"
            )

            return {
                "entities": []
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

            parsed = json.loads(
                cleaned
            )

            return {
                "entities": parsed.get(
                    "entities",
                    []
                )
            }

        except Exception:
            return {
                "entities": []
            }
