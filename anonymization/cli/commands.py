import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from anonymization.core.anonymizer import Anonymizer
from anonymization.cli.file_handlers import get_file_handler, ExcelFileHandler
from anonymization.cli.config_builder import InteractiveConfigBuilder, FileConfigBuilder


class Command(ABC):
    
    @abstractmethod
    def execute(self) -> None:
        pass


class ShowColumnsCommand(Command):
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def execute(self) -> None:
        file_handler = get_file_handler(self.file_path)
        file_handler.show_info()


class AnonymizeCommand(Command):
    
    def __init__(self,
                 input_path: str,
                 output_path: str,
                 config_path: Optional[str] = None,
                 interactive: bool = False,
                 salt: Optional[str] = None,
                 locale: str = 'en_US',
                 show_salt: bool = False):
        self.input_path = input_path
        self.output_path = output_path
        self.config_path = config_path
        self.interactive = interactive
        self.salt = salt
        self.locale = locale
        self.show_salt = show_salt
    
    def execute(self) -> None:
        column_config = self._build_config()
        
        if not column_config:
            print("No columns configured for anonymization. Exiting.")
            sys.exit(1)
        
        print(f"\nColumn configuration:")
        for col, col_type in column_config.items():
            print(f"  {col} -> {col_type}")
        
        salt_bytes = bytes.fromhex(self.salt) if self.salt else None
        
        anonymizer = Anonymizer(
            column_config=column_config,
            salt=salt_bytes,
            locale=self.locale
        )
        
        self._anonymize_file(anonymizer)
        
        print(f"\n✓ Anonymized file saved to: {self.output_path}")
        
        if self.show_salt:
            salt_hex = anonymizer.get_salt().hex()
            print(f"\nSalt (save for reproducibility): {salt_hex}")
    
    def _build_config(self) -> dict[str, str]:
        if self.config_path:
            builder = FileConfigBuilder(self.config_path)
            print(f"Loaded configuration from: {self.config_path}")
            return builder.build()
        elif self.interactive:
            file_handler = get_file_handler(self.input_path)
            
            if isinstance(file_handler, ExcelFileHandler):
                print("\nDetecting unique columns across all Excel sheets...")
                print("(The configuration will apply to all sheets)")
            
            columns = file_handler.detect_columns()
            builder = InteractiveConfigBuilder(columns)
            return builder.build()
        else:
            print("Error: Must specify either --config or --interactive")
            sys.exit(1)
    
    def _anonymize_file(self, anonymizer: Anonymizer) -> None:
        input_path = Path(self.input_path)
        suffix = input_path.suffix.lower()
        
        if suffix == '.csv':
            anonymizer.anonymize_csv(self.input_path, self.output_path)
        elif suffix in ['.xlsx', '.xls']:
            anonymizer.anonymize_excel(self.input_path, self.output_path)
        else:
            print(f"Error: Unsupported file format: {suffix}")
            sys.exit(1)
