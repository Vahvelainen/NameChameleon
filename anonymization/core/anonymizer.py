from typing import Dict, Optional, Any
import pandas as pd
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.normalizer import StringNormalizer
from anonymization.utils.name_generator import NameGenerator
from anonymization.core.column_handlers import (
    FirstNameHandler,
    LastNameHandler,
    FullNameHandler,
    EmailHandler,
    IdHandler,
    MiscHandler
)


class Anonymizer:
    
    def __init__(self, 
                 column_config: Dict[str, str],
                 salt: Optional[bytes] = None,
                 locale: str = 'en_US'):
        pass
    
    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
    
    def anonymize_csv(self, input_path: str, output_path: str) -> None:
        pass
    
    def anonymize_excel(self, input_path: str, output_path: str) -> None:
        pass
    
    def get_salt(self) -> bytes:
        pass

