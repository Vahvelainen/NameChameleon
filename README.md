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

## Usage

```python
from anonymization.core.anonymizer import Anonymizer

# Map your column names to anonymization types
column_config = {
    'FirstName': 'first_name',      # Column name in your file → type
    'LastName': 'last_name',
    'Email': 'email',
    'EmployeeID': 'id',
    'Notes': 'misc'
    # Columns not listed here remain unchanged
}

anonymizer = Anonymizer(column_config=column_config, locale='en_US')

# Excel (processes all sheets)
anonymizer.anonymize_excel('input.xlsx', 'output.xlsx')

# CSV
anonymizer.anonymize_csv('input.csv', 'output.csv')

# Save salt for reproducibility (optional)
salt = anonymizer.get_salt()
print(f"Salt: {salt.hex()}")

# Reuse salt for consistent results
anonymizer2 = Anonymizer(column_config=column_config, salt=salt)
```

## Column Types

- `first_name`: Anonymizes to realistic first names
- `last_name`: Anonymizes to realistic last names
- `full_name`: Anonymizes full names (splits and handles independently)
- `email`: Generates email from anonymized names (see below)
- `id`: Hashes to 8-character alphanumeric ID
- `misc`: Replaces with empty string (deletes)

**Note:** Columns not in `column_config` remain unchanged.

### Email Handling

Email anonymization preserves the domain and only treats dot (`.`) as a name separator:

```
john.smith@company.com    → michael.jones@company.com    (two parts: first.last)
alice@example.com         → sarah@example.com            (single name)
alice_johnson@company.com → sarah@company.com            (underscore NOT a separator)
```

For consistency across columns, use dot-separated emails (e.g., `john.smith@domain.com`) that match your `FirstName` and `LastName` columns.

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

