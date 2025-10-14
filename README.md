# NameChameleon

A Python tool for anonymizing Excel and CSV files with deterministic pseudonymization.

## Features

- Deterministic anonymization using salted HMAC-SHA256
- Support for multiple column types: first_name, last_name, full_name, full_name_inverted, email, id, misc
- Excel multi-sheet support
- Extensible OOP architecture
- Dynamic name generation using Faker

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .  # Install CLI tool
```

## Usage

### CLI Tool

```bash
# Interactive mode - select column types interactively
namemasker anonymize input.xlsx output.xlsx -i

# Using a config file
namemasker anonymize input.csv output.csv -c examples/config.json

# Show available columns in a file
namemasker columns input.xlsx

# With salt for reproducibility
namemasker anonymize input.csv output.csv -c config.json --salt a1b2c3d4... --show-salt

# Different locale
namemasker anonymize input.xlsx output.xlsx -i --locale fi_FI
```

### Python API

```python
from anonymization import Anonymizer

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

#### Input
| FirstName | LastName | FullName | Email | EmployeeID | Department | Notes |
|-----------|----------|----------|-------|------------|------------|-------|
| John | Smith | John Smith | john.smith@company.com | EMP001 | Engineering | Private info 1 |
| Alice | Johnson | Alice Johnson | alice.johnson@company.com | EMP002 | Sales | Confidential 2 |
| Bob | Anderson | Bob Anderson | bob.anderson@example.org | EMP003 | Marketing | Secret 3 |
| Mary | Brown | Mary Brown | mary.brown@company.com | EMP004 | Engineering | Internal 4 |

#### Output
| FirstName | LastName | FullName | Email | EmployeeID | Department | Notes |
|-----------|----------|----------|-------|------------|------------|-------|
| Patrick | Lowe | Patrick Lowe | patrick.lowe@company.com | JQ3O81FS | Engineering | |
| Jason | Williams | Jason Williams | jason.williams@company.com | 0CB4RISP | Sales | |
| Sheila | Flores | Sheila Flores | sheila.flores@example.org | 0VQ5XJRZ | Marketing | |
| Lauren | Bush | Lauren Bush | lauren.bush@company.com | XBIGNGA8 | Engineering | |

*Note: Department column remains unchanged (not in column_config), while Notes are cleared (misc type).*

## Column Types

- `first_name`: Anonymizes to realistic first names
- `last_name`: Anonymizes to realistic last names
- `full_name`: Anonymizes full names in natural order (First Middle... Last)
  - Example: `"John Michael Smith"` → `"Jennifer Emily Thompson"`
  - Single name treated as first name
- `full_name_inverted`: Anonymizes full names in inverted order (Last First Middle...)
  - Example: `"Smith John Michael"` → `"Thompson Jennifer Emily"`
  - Single name treated as last name
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

