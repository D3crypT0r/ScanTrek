import os
import yaml
import json
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

class ConfigLoader:
    def __init__(self):
        self.config = {}
        self._load_environment()
        self._load_yaml_config()
        self._validate_config()

    def _load_environment(self):
        load_dotenv("config/.env")
        self.env_vars = {
            "database_url": os.getenv("DATABASE_URL"),
            "virustotal_key": os.getenv("VIRUSTOTAL_API_KEY"),
            "shodan_key": os.getenv("SHODAN_API_KEY")
        }

    def _load_yaml_config(self):
        with open("config/default.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        self._merge_env_vars()

    def _merge_env_vars(self):
        # Replace ${VAR} patterns in YAML with actual environment values
        for section in self.config.values():
            if isinstance(section, dict):
                for key, value in section.items():
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        var_name = value[2:-1]
                        section[key] = os.getenv(var_name, "")

    def _validate_config(self):
        with open("config/schema.json", "r") as f:
            schema = json.load(f)
        
        class ConfigModel(BaseModel):
            crawler: dict
            analysis: dict
            stealth: dict = None
            reporting: dict = None
            integrations: dict = None

        try:
            ConfigModel(**self.config)
        except ValidationError as e:
            print(f"Configuration error: {str(e)}")
            raise

    def get(self, path: str, default=None):
        keys = path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key)
            if value is None:
                return default
        return value
