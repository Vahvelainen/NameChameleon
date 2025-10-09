from typing import Any, Dict, Set
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.normalizer import StringNormalizer
from anonymization.utils.name_generator import NameGenerator


class BaseColumnHandler:
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer):
        pass
    
    def anonymize(self, value: Any) -> Any:
        pass


class FirstNameHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        pass
    
    def anonymize(self, value: Any) -> Any:
        pass


class LastNameHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        pass
    
    def anonymize(self, value: Any) -> Any:
        pass


class FullNameHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        pass
    
    def anonymize(self, value: Any) -> Any:
        pass


class EmailHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        pass
    
    def anonymize(self, value: Any) -> Any:
        pass


class IdHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer):
        pass
    
    def anonymize(self, value: Any) -> str:
        pass


class MiscHandler(BaseColumnHandler):
    
    def anonymize(self, value: Any) -> str:
        pass

