from typing import Dict
from faker import Faker
from faker.exceptions import UniquenessException


class NameGenerator:
    
    def __init__(self, locale: str = 'en_US', seed: int = None):
        self.locale = locale
        self.faker = Faker(self.locale)
        if seed is not None:
            self.faker.seed_instance(seed)
        self.first_name_cache: Dict[int, str] = {}
        self.last_name_cache: Dict[int, str] = {}
        self.suffix_counter_first: Dict[str, int] = {}
        self.suffix_counter_last: Dict[str, int] = {}
    
    def get_first_name(self, hash_int: int) -> str:
        if hash_int in self.first_name_cache:
            return self.first_name_cache[hash_int]
        
        try:
            name = self.faker.unique.first_name()
        except UniquenessException:
            temp_faker = Faker(self.locale)
            temp_faker.seed_instance(hash_int)
            base_name = temp_faker.first_name()
            
            if base_name not in self.suffix_counter_first:
                self.suffix_counter_first[base_name] = 2
            else:
                self.suffix_counter_first[base_name] += 1
            
            name = f"{base_name}{self.suffix_counter_first[base_name]}"
        
        self.first_name_cache[hash_int] = name
        return name
    
    def get_last_name(self, hash_int: int) -> str:
        if hash_int in self.last_name_cache:
            return self.last_name_cache[hash_int]
        
        try:
            name = self.faker.unique.last_name()
        except UniquenessException:
            temp_faker = Faker(self.locale)
            temp_faker.seed_instance(hash_int)
            base_name = temp_faker.last_name()
            
            if base_name not in self.suffix_counter_last:
                self.suffix_counter_last[base_name] = 2
            else:
                self.suffix_counter_last[base_name] += 1
            
            name = f"{base_name}{self.suffix_counter_last[base_name]}"
        
        self.last_name_cache[hash_int] = name
        return name

