from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import pandas as pd


class FileHandler(ABC):
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.path = Path(file_path)
        self._validate_file()
    
    def _validate_file(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
    
    @abstractmethod
    def detect_columns(self) -> list[str]:
        pass
    
    @abstractmethod
    def show_info(self) -> None:
        pass


class CsvFileHandler(FileHandler):
    
    def detect_columns(self) -> list[str]:
        df = pd.read_csv(self.file_path, nrows=0)
        return df.columns.tolist()
    
    def show_info(self) -> None:
        columns = self.detect_columns()
        print(f"\nColumns in '{self.file_path}':")
        for i, col in enumerate(columns, 1):
            print(f"  {i}. {col}")
        print()


class ExcelFileHandler(FileHandler):
    
    def detect_columns(self) -> list[str]:
        xl = pd.ExcelFile(self.file_path)
        all_columns = []
        seen = set()
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name, nrows=0)
            for col in df.columns:
                if col not in seen:
                    all_columns.append(col)
                    seen.add(col)
        
        return all_columns
    
    def show_info(self) -> None:
        xl = pd.ExcelFile(self.file_path)
        print(f"\nColumns in '{self.file_path}':")
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name, nrows=0)
            print(f"\n  Sheet: {sheet_name}")
            for i, col in enumerate(df.columns, 1):
                print(f"    {i}. {col}")
        
        print(f"\n  Unique columns across all sheets:")
        unique_cols = self.detect_columns()
        for i, col in enumerate(unique_cols, 1):
            print(f"    {i}. {col}")
        print()


def get_file_handler(file_path: str) -> FileHandler:
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    if suffix == '.csv':
        return CsvFileHandler(file_path)
    elif suffix in ['.xlsx', '.xls']:
        return ExcelFileHandler(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

