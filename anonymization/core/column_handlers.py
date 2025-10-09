from typing import Any
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.normalizer import StringNormalizer
from anonymization.utils.name_generator import NameGenerator


class BaseColumnHandler:
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer):
        self.hasher = hasher
        self.normalizer = normalizer
    
    def anonymize(self, value: Any) -> Any:
        raise NotImplementedError


class FirstNameHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        super().__init__(hasher, normalizer)
        self.name_generator = name_generator
    
    def anonymize(self, value: Any) -> str:
        normalized = self.normalizer.normalize(value)
        if not normalized:
            return ""
        
        hash_int = self.hasher.hash_to_int(normalized)
        return self.name_generator.get_first_name(hash_int)


class LastNameHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        super().__init__(hasher, normalizer)
        self.name_generator = name_generator
    
    def anonymize(self, value: Any) -> str:
        normalized = self.normalizer.normalize(value)
        if not normalized:
            return ""
        
        hash_int = self.hasher.hash_to_int(normalized)
        return self.name_generator.get_last_name(hash_int)


class FullNameHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        super().__init__(hasher, normalizer)
        self.name_generator = name_generator
    
    def anonymize(self, value: Any) -> str:
        normalized = self.normalizer.normalize(value)
        if not normalized:
            return ""
        
        parts = normalized.split()
        if len(parts) == 0:
            return ""
        elif len(parts) == 1:
            hash_int = self.hasher.hash_to_int(parts[0])
            return self.name_generator.get_first_name(hash_int)
        else:
            first_hash = self.hasher.hash_to_int(parts[0])
            last_hash = self.hasher.hash_to_int(parts[-1])
            first = self.name_generator.get_first_name(first_hash)
            last = self.name_generator.get_last_name(last_hash)
            return f"{first} {last}"


class EmailHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer, name_generator: NameGenerator):
        super().__init__(hasher, normalizer)
        self.name_generator = name_generator
    
    def anonymize(self, value: Any) -> str:
        normalized = self.normalizer.normalize(value)
        if not normalized or '@' not in normalized:
            return ""
        
        local_part, domain = normalized.split('@', 1)
        
        parts = local_part.split('.')
        
        if len(parts) == 0 or (len(parts) == 1 and not parts[0]):
            return ""
        elif len(parts) == 1:
            hash_int = self.hasher.hash_to_int(parts[0])
            first = self.name_generator.get_first_name(hash_int)
            email = f"{first.lower()}@{domain}"
        else:
            first_hash = self.hasher.hash_to_int(parts[0])
            last_hash = self.hasher.hash_to_int(parts[-1])
            first = self.name_generator.get_first_name(first_hash)
            last = self.name_generator.get_last_name(last_hash)
            email = f"{first.lower()}.{last.lower()}@{domain}"
        
        return email


class IdHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer):
        super().__init__(hasher, normalizer)
    
    def anonymize(self, value: Any) -> str:
        normalized = self.normalizer.normalize(value)
        if not normalized:
            return ""
        
        hash_int = self.hasher.hash_to_int(normalized)
        
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base = len(chars)
        result = []
        
        for _ in range(8):
            result.append(chars[hash_int % base])
            hash_int //= base
        
        return ''.join(result)


class MiscHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: StringNormalizer):
        super().__init__(hasher, normalizer)
    
    def anonymize(self, value: Any) -> str:
        return ""

