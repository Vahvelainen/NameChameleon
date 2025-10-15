from typing import Any, Dict
import pandas as pd
from anonymization import (
    Anonymizer,
    BaseColumnHandler,
    DeterministicHasher,
    IdNormalizer
)


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
    
    def get_handlers(self) -> Dict[str, BaseColumnHandler]:
        # Get all standard handlers
        handlers = super().get_handlers()
        
        # Add custom handler
        handlers['employee_id'] = EmployeeIdHandler(self.hasher, self.id_normalizer)
        
        return handlers


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

