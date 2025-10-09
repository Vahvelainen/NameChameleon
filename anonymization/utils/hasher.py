from typing import Optional


class DeterministicHasher:
    
    def __init__(self, salt: Optional[bytes] = None):
        pass
    
    def hash_to_int(self, value: str, domain_size: int) -> int:
        pass
    
    def get_salt(self) -> bytes:
        pass

