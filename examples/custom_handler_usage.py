from typing import Any
import pandas as pd
from anonymization.core.anonymizer import Anonymizer
from anonymization.core.column_handlers import (
    BaseColumnHandler,
    FirstNameHandler,
    LastNameHandler,
    FullNameHandler,
    FullNameInvertedHandler,
    EmailHandler,
    IdHandler,
    MiscHandler
)
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.normalizer import IdNormalizer


# Custom handler for employee IDs with format EID-XXXX
class EmployeeIdHandler(BaseColumnHandler):
    
    def __init__(self, hasher: DeterministicHasher, normalizer: IdNormalizer):
        super().__init__(hasher, normalizer)
    
    def anonymize(self, value: Any) -> str:
        # Normalize the input value
        normalized = self.normalizer.normalize(value)
        if not normalized:
            return ""
        
        # Generate a deterministic hash
        hash_int = self.hasher.hash_to_int(normalized)
        
        # Generate 4 digits from the hash
        digits = str(hash_int % 10000).zfill(4)
        
        # Return in EID-XXXX format
        return f"EID-{digits}"


# Extend Anonymizer to support custom handlers
class CustomAnonymizer(Anonymizer):
    
    def _initialize_handlers(self) -> None:
        # Build handler map with both standard and custom handlers
        handler_map = {
            'first_name': FirstNameHandler(self.hasher, self.normalizer, self.name_generator),
            'last_name': LastNameHandler(self.hasher, self.normalizer, self.name_generator),
            'full_name': FullNameHandler(self.hasher, self.normalizer, self.name_generator),
            'full_name_inverted': FullNameInvertedHandler(self.hasher, self.normalizer, self.name_generator),
            'email': EmailHandler(self.hasher, self.normalizer, self.name_generator),
            'id': IdHandler(self.hasher, self.id_normalizer),
            'misc': MiscHandler(self.hasher, self.normalizer),
            # Add custom handler
            'employee_id': EmployeeIdHandler(self.hasher, self.id_normalizer)
        }
        
        # Map columns to their handlers
        for column_name, column_type in self.column_config.items():
            if column_type not in handler_map:
                raise ValueError(f"Unknown column type: {column_type}")
            self.handlers[column_name] = handler_map[column_type]


# Example usage
if __name__ == "__main__":
    # Create sample data
    data = {
        'FirstName': ['John', 'Jane', 'Bob'],
        'LastName': ['Doe', 'Smith', 'Johnson'],
        'Email': ['john.doe@company.com', 'jane.smith@company.com', 'bob.johnson@company.com'],
        'EmployeeID': ['EID-1234', 'EID-5678', 'EID-9012']
    }
    df = pd.DataFrame(data)
    
    # Configuration using custom handler type
    column_config = {
        'FirstName': 'first_name',
        'LastName': 'last_name',
        'Email': 'email',
        'EmployeeID': 'employee_id'  # Maps to our custom handler
    }
    
    # Create anonymizer with custom handler support
    anonymizer = CustomAnonymizer(
        column_config=column_config,
        locale='en_US'
    )
    
    # Anonymize the data
    anonymized_df = anonymizer.anonymize_dataframe(df)
    
    print("Original Data:")
    print(df)
    print("\nAnonymized Data:")
    print(anonymized_df)
    print(f"\nSalt: {anonymizer.get_salt().hex()}")

