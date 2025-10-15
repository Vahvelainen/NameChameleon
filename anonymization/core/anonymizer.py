from typing import Dict, Optional
import pandas as pd
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.normalizer import StringNormalizer, IdNormalizer
from anonymization.utils.name_generator import NameGenerator
from anonymization.core.column_handlers import (
    FirstNameHandler,
    LastNameHandler,
    FullNameHandler,
    FullNameInvertedHandler,
    EmailHandler,
    IdHandler,
    MiscHandler,
    BaseColumnHandler
)


class Anonymizer:
    
    def __init__(self, 
                 column_config: Dict[str, str],
                 salt: Optional[bytes] = None,
                 locale: str = 'en_US'):
        self.column_config = column_config
        self.locale = locale
        
        self.hasher = DeterministicHasher(salt)
        
        salt_bytes = self.hasher.get_salt()
        seed = int.from_bytes(salt_bytes[:8])
        self.name_generator = NameGenerator(locale, seed=seed)
        
        self.handlers: Dict[str, BaseColumnHandler] = {}
        self._initialize_handlers()
    
    def get_handlers(self) -> Dict[str, BaseColumnHandler]:
        normalizer = StringNormalizer()
        id_normalizer = IdNormalizer()
        
        return {
            'first_name': FirstNameHandler(self.hasher, normalizer, self.name_generator),
            'last_name': LastNameHandler(self.hasher, normalizer, self.name_generator),
            'full_name': FullNameHandler(self.hasher, normalizer, self.name_generator),
            'full_name_inverted': FullNameInvertedHandler(self.hasher, normalizer, self.name_generator),
            'email': EmailHandler(self.hasher, normalizer, self.name_generator),
            'id': IdHandler(self.hasher, id_normalizer),
            'misc': MiscHandler(self.hasher, normalizer)
        }
    
    def _initialize_handlers(self) -> None:
        handler_map = self.get_handlers()
        
        for column_name, column_type in self.column_config.items():
            if column_type not in handler_map:
                raise ValueError(f"Unknown column type: {column_type}")
            self.handlers[column_name] = handler_map[column_type]
    
    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        result_df = df.copy()
        
        for column_name, handler in self.handlers.items():
            if column_name in result_df.columns:
                result_df[column_name] = result_df[column_name].apply(handler.anonymize)
        
        return result_df
    
    def anonymize_csv(self, input_path: str, output_path: str) -> None:
        df = pd.read_csv(input_path)
        anonymized_df = self.anonymize_dataframe(df)
        anonymized_df.to_csv(output_path, index=False)
    
    def anonymize_excel(self, input_path: str, output_path: str) -> None:
        excel_file = pd.ExcelFile(input_path)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                anonymized_df = self.anonymize_dataframe(df)
                anonymized_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    def get_salt(self) -> bytes:
        return self.hasher.get_salt()

