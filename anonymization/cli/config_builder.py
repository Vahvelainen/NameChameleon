from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Dict, Any


COLUMN_TYPES = ['first_name', 'last_name', 'full_name', 'full_name_inverted', 'email', 'id', 'misc', 'skip']


class ConfigBuilder(ABC):
    
    @abstractmethod
    def build(self) -> Dict[str, str]:
        pass


class InteractiveConfigBuilder(ConfigBuilder):
    
    def __init__(self, columns: list[str]):
        self.columns = columns
    
    def build(self) -> Dict[str, str]:
        print("\nAvailable column types:")
        for i, col_type in enumerate(COLUMN_TYPES, 1):
            print(f"  {i}. {col_type}")
        
        print("\nMap your columns to types (or 'skip' to leave unchanged):\n")
        
        column_config = {}
        for column in self.columns:
            while True:
                choice = input(f"'{column}' -> type (1-{len(COLUMN_TYPES)}) or name: ").strip().lower()
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(COLUMN_TYPES):
                        col_type = COLUMN_TYPES[idx]
                        if col_type != 'skip':
                            column_config[column] = col_type
                        break
                    else:
                        print(f"Invalid choice. Enter 1-{len(COLUMN_TYPES)}")
                elif choice in COLUMN_TYPES:
                    if choice != 'skip':
                        column_config[column] = choice
                    break
                elif choice == '':
                    break
                else:
                    print(f"Invalid type. Choose from: {', '.join(COLUMN_TYPES)}")
        
        return column_config


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

