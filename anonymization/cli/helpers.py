import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd


COLUMN_TYPES = ['first_name', 'last_name', 'full_name', 'full_name_inverted', 'email', 'id', 'misc', 'skip']


def detect_file_columns(file_path: str) -> list[str]:
    path = Path(file_path)
    if path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path, nrows=0)
        return df.columns.tolist()
    elif path.suffix.lower() in ['.xlsx', '.xls']:
        xl = pd.ExcelFile(file_path)
        all_columns = []
        seen = set()
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=0)
            for col in df.columns:
                if col not in seen:
                    all_columns.append(col)
                    seen.add(col)
        
        return all_columns
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def interactive_column_mapping(columns: list[str]) -> Dict[str, str]:
    print("\nAvailable column types:")
    for i, col_type in enumerate(COLUMN_TYPES, 1):
        print(f"  {i}. {col_type}")
    
    print("\nMap your columns to types (or 'skip' to leave unchanged):\n")
    
    column_config = {}
    for column in columns:
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


def load_config_file(config_path: str) -> Dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(path, 'r') as f:
        config = json.load(f)
    
    return config.get('column_config', {})

