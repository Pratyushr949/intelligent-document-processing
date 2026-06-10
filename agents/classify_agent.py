import logging
from typing import Any, Dict

from agents.base import BaseDocumentAgent
from config.config_loader import settings

logger = logging.getLogger("agents.classify")


class DocumentClassifyAgent(BaseDocumentAgent):
    """
    Agent responsible for classifying documents into predefined categories.
    """

    def __init__(self, **kwargs):
        categories = (
            settings.yaml_config
            .get("classification", {})
            .get(
                "categories",
                ["invoice", "receipt", "contract", "other"]
            )
        )

        instruction = (
            f"You are a document classifier. "
            f"Classify the input document into one of the following "
            f"categories: {', '.join(categories)}. "
            f"Provide the predicted category and confidence level."
        )

        super().__init__(
            name="classify_agent",
            instruction=instruction,
            **kwargs
        )

    def process_document(
        self,
        file_path: str,
        **kwargs
    ) -> Dict[str, Any]:

        self._logger.info(
            f"Running Classification Agent on document: {file_path}"
        )

        return {
            "status": "success",
            "file_path": file_path,
            "predicted_category": "other",
            "confidence": 0.90
        }
