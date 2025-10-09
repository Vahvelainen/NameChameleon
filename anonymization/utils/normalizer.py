import unicodedata
from typing import Any


class StringNormalizer:
    
    @staticmethod
    def normalize(value: Any) -> str:
        if value is None or (isinstance(value, float) and value != value):
            return ""
        
        text = str(value)
        text = unicodedata.normalize('NFKC', text)
        text = text.strip()
        text = text.casefold()
        
        return text

