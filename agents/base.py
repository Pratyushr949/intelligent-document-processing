from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, Optional

from config.config_loader import settings

# Google ADK
try:
    from google.adk.agents import Agent
    from pydantic import PrivateAttr

    HAS_GOOGLE_ADK = True

except ImportError:
    HAS_GOOGLE_ADK = False

    class Agent:
        def __init__(self, name: str, model: str, instruction: str, **kwargs):
            self.name = name
            self.model = model
            self.instruction = instruction
            self.kwargs = kwargs

        def run(self, *args, **kwargs):
            return "Mock execution output"

    class PrivateAttr:
        def __init__(self, default=None):
            self.default = default


logger = logging.getLogger("agents.base")


class BaseDocumentAgent(Agent, ABC):
    """
    Base class for all document intelligence agents.
    """

    _logger = PrivateAttr(default=None)

    def __init__(
        self,
        name: str,
        instruction: str,
        model: Optional[str] = None,
        **kwargs
    ):
        # Get model from config
        default_model = (
            settings.yaml_config
            .get("gemini", {})
            .get("default_model", "gemini-2.5-flash")
        )

        model_name = model or default_model

        # IMPORTANT:
        # Current Google ADK Agent does NOT accept temperature
        super().__init__(
            name=name,
            model=model_name,
            instruction=instruction,
            **kwargs
        )

        self._logger = logging.getLogger(f"agents.{name}")

        self._logger.info(
            f"Initialized agent '{name}' "
            f"with model '{model_name}' "
            f"(Google ADK Available: {HAS_GOOGLE_ADK})"
        )

    @abstractmethod
    def process_document(
        self,
        file_path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process a document and return structured results.

        Args:
            file_path: Path to input document

        Returns:
            Structured processing results
        """
        pass