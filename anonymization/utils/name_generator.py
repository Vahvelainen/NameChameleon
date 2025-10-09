from typing import Set, Dict
from faker import Faker


class NameGenerator:
    
    def __init__(self, locale: str = 'en_US'):
        self.locale = locale
        self.used_first_names: Set[str] = set()
        self.used_last_names: Set[str] = set()
        self.first_name_cache: Dict[int, str] = {}
        self.last_name_cache: Dict[int, str] = {}
    
    def get_first_name(self, hash_int: int) -> str:
        if hash_int in self.first_name_cache:
            return self.first_name_cache[hash_int]
        
        attempt = 0
        while True:
            faker = Faker(self.locale)
            faker.seed_instance(hash_int + attempt)
            name = faker.first_name()
            
            if name not in self.used_first_names:
                self.used_first_names.add(name)
                self.first_name_cache[hash_int] = name
                return name
            
            attempt += 1
    
    def get_last_name(self, hash_int: int) -> str:
        if hash_int in self.last_name_cache:
            return self.last_name_cache[hash_int]
        
        attempt = 0
        while True:
            faker = Faker(self.locale)
            faker.seed_instance(hash_int + attempt)
            name = faker.last_name()
            
            if name not in self.used_last_names:
                self.used_last_names.add(name)
                self.last_name_cache[hash_int] = name
                return name
            
            attempt += 1

