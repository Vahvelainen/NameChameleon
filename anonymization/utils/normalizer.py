import unicodedata
from typing import Any
import pandas as pd


class StringNormalizer:
    
    @staticmethod
    def normalize(value: Any) -> str:
        if value is None or pd.isna(value):
            return ""
        
        text = str(value)
        text = unicodedata.normalize('NFKC', text)
        text = text.strip()
        text = text.casefold()
        
        return text


class IdNormalizer:
    
    @staticmethod
    def normalize(value: Any) -> str:
        if value is None or pd.isna(value):
            return ""
        
        return str(value).strip()

