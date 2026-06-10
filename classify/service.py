import logging
from typing import Any, Dict
from agents.classify_agent import DocumentClassifyAgent

logger = logging.getLogger("classify.service")


class ClassificationService:
    """
    Service responsible for orchestrating document classification.
    Integrates with the DocumentClassifyAgent to determine document types.
    """

    def __init__(self):
        self.agent = DocumentClassifyAgent()
        logger.info("Classification Service initialized with DocumentClassifyAgent.")

    def run_classification(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Executes classification skeleton for the given document path.
        Logs the process and delegates to the underlying agent.
        """
        logger.info(f"Initiating classification service task for document: {file_path}")
        
        try:
            # Delegate task execution to the agent
            result = self.agent.process_document(file_path, **kwargs)
            logger.info(f"Classification service task completed successfully for file: {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error encountered during classification service execution for file {file_path}: {e}")
            return {
                "agent": self.agent.name,
                "status": "error",
                "file_processed": file_path,
                "error": str(e)
            }
