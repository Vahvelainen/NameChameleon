from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Dict

from anonymization.cli.interactive_column_mapper import ColumnMappingUI


class ConfigBuilder(ABC):
    
    @abstractmethod
    def build(self) -> Dict[str, str]:
        pass


class InteractiveConfigBuilder(ConfigBuilder):
    
    def __init__(self, columns: list[str]):
        self.columns = columns
    
    def build(self) -> Dict[str, str]:
        ui = ColumnMappingUI(self.columns)
        return ui.run()


class FileConfigBuilder(ConfigBuilder):
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.path = Path(config_path)
        self._validate_file()
    
    def _validate_file(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
    
    def build(self) -> Dict[str, str]:
        with open(self.path, 'r') as f:
            config = json.load(f)
        
        return config.get('column_config', {})

