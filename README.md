# NameMasker

A Python tool for anonymizing Excel and CSV files with deterministic pseudonymization.

## Features

- Deterministic anonymization using salted HMAC-SHA256
- Support for multiple column types: first_name, last_name, full_name, email, id, misc
- Excel multi-sheet support
- Extensible OOP architecture
- Dynamic name generation using Faker

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage Example

```python
from anonymization.core.anonymizer import Anonymizer

column_config = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'Email': 'email',
    'EmployeeID': 'id',
    'Notes': 'misc'
}

anonymizer = Anonymizer(column_config=column_config, locale='en_US')

anonymizer.anonymize_excel('input.xlsx', 'output.xlsx')

print(f"Salt used: {anonymizer.get_salt().hex()}")
```

## Column Types

- `first_name`: Anonymizes to realistic first names
- `last_name`: Anonymizes to realistic last names
- `full_name`: Anonymizes full names (splits and handles independently)
- `email`: Generates email from anonymized names
- `id`: Hashes to 8-character alphanumeric ID
- `misc`: Replaces with empty string (deletes)

## Architecture

```
anonymization/
├── core/
│   ├── anonymizer.py        # Main Anonymizer class
│   └── column_handlers.py   # Handler for each column type
└── utils/
    ├── normalizer.py        # String normalization
    ├── hasher.py            # Deterministic hashing
    └── name_generator.py    # Dynamic name generation
```

