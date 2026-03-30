import hmac
import hashlib
import secrets
from typing import Optional


class DeterministicHasher:
    
    def __init__(self, salt: Optional[bytes] = None):
        if salt is None:
            self.salt = secrets.token_bytes(32)
        else:
            self.salt = salt
    
    def hash_to_int(self, value: str) -> int:
        digest = hmac.new(
            self.salt,
            value.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return int.from_bytes(digest, byteorder='big')
    
    def get_salt(self) -> bytes:
        return self.salt

