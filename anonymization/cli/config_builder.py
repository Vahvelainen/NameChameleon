from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Dict, Any

from anonymization.cli.interactive_colum_mapper import ColumnMappingUI, COLUMN_TYPES


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
        
        column_config = config.get('column_config', {})
        
        self._validate_config(column_config)
        
        return column_config
    
    def _validate_config(self, column_config: Dict[str, Any]) -> None:
        valid_types = set(COLUMN_TYPES) - {'skip'}
        
        for column, col_type in column_config.items():
            if col_type not in valid_types:
                raise ValueError(f"Invalid column type '{col_type}' for column '{column}'. Valid types: {', '.join(valid_types)}")

