import os
import logging
import logging.config
from pathlib import Path
from typing import Any, Dict
import yaml
from dotenv import load_dotenv

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()

logger = logging.getLogger("config_loader")


class Settings:
    """Application Settings holding configuration from YAML and environment variables."""

    def __init__(self):
        self.base_dir: Path = BASE_DIR
        self.env: str = os.getenv("ENV", "development")
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Load configuration path
        config_path_str = os.getenv("CONFIG_PATH", "config/config.yaml")
        self.config_path: Path = BASE_DIR / config_path_str
        
        # Parse YAML configuration
        self.yaml_config: Dict[str, Any] = self._load_yaml_config()
        self._merge_env_overrides()

        # Initialize logging
        self._setup_logging()

    def _load_yaml_config(self) -> Dict[str, Any]:
        """Loads configuration from YAML file."""
        if not self.config_path.exists():
            # Standard default fallback if config file is missing
            return {
                "app": {"title": "Document Intelligence System", "version": "1.0.0"},
                "gemini": {"default_model": "gemini-2.5-flash", "temperature": 0.1},
                "storage": {"input_dir": "data/input", "processed_dir": "data/processed", "output_json_dir": "outputs/json"}
            }
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading configuration from {self.config_path}: {e}")
            return {}

    def _merge_env_overrides(self):
        """Overrides yaml_config values with environment variable specifications."""
        # Ensure base structure exists
        if "gemini" not in self.yaml_config:
            self.yaml_config["gemini"] = {}
        if "storage" not in self.yaml_config:
            self.yaml_config["storage"] = {}

        # Merge environment overrides into yaml_config dict
        if self.gemini_api_key:
            self.yaml_config["gemini"]["api_key"] = self.gemini_api_key
        
        # Adjust storage paths to absolute paths
        input_dir = self.yaml_config["storage"].get("input_dir", "data/input")
        processed_dir = self.yaml_config["storage"].get("processed_dir", "data/processed")
        output_dir = self.yaml_config["storage"].get("output_json_dir", "outputs/json")

        self.input_path = self.base_dir / input_dir
        self.processed_path = self.base_dir / processed_dir
        self.output_path = self.base_dir / output_dir

        # Ensure folders exist
        self.input_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        """Initializes application logging using the config/logging.yaml schema."""
        logging_config_path = self.base_dir / "config" / "logging.yaml"
        if logging_config_path.exists():
            try:
                with open(logging_config_path, "r", encoding="utf-8") as f:
                    log_cfg = yaml.safe_load(f)
                    
                # Dynamically set level in logging config from env if specified
                if "root" in log_cfg:
                    log_cfg["root"]["level"] = self.log_level
                    
                # Configure file path to go under the base dir
                if "handlers" in log_cfg and "file" in log_cfg["handlers"]:
                    log_file = log_cfg["handlers"]["file"].get("filename", "document_intelligence.log")
                    log_cfg["handlers"]["file"]["filename"] = str(self.base_dir / log_file)

                logging.config.dictConfig(log_cfg)
                logging.getLogger("config_loader").info("Logging successfully configured from logging.yaml")
            except Exception as e:
                logging.basicConfig(level=logging.INFO)
                logging.getLogger("config_loader").warning(f"Failed to load logging config from yaml: {e}. Defaulted to basic config.")
        else:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger("config_loader").info("logging.yaml not found. Configured fallback basic logging.")


# Single instance export for app-wide settings loading
settings = Settings()
