import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anonymization.utils.normalizer import StringNormalizer
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.name_generator import NameGenerator
from anonymization.core.column_handlers import (
    FirstNameHandler,
    LastNameHandler,
    FullNameHandler,
    EmailHandler,
    IdHandler,
    MiscHandler
)

normalizer = StringNormalizer()
hasher = DeterministicHasher()
name_gen = NameGenerator(locale='en_US')

first_handler = FirstNameHandler(hasher, normalizer, name_gen)
last_handler = LastNameHandler(hasher, normalizer, name_gen)
full_handler = FullNameHandler(hasher, normalizer, name_gen)
email_handler = EmailHandler(hasher, normalizer, name_gen)
id_handler = IdHandler(hasher, normalizer)
misc_handler = MiscHandler(hasher, normalizer)

print("=" * 80)
print("Testing Column Handlers")
print("=" * 80)

test_records = [
    {
        "FirstName": "John",
        "LastName": "Smith",
        "FullName": "John Smith",
        "Email": "john.smith@company.com",
        "EmployeeID": "EMP001",
        "Notes": "Some confidential info"
    },
    {
        "FirstName": "Alice",
        "LastName": "Johnson",
        "FullName": "Alice Johnson",
        "Email": "alice.johnson@company.com",
        "EmployeeID": "EMP002",
        "Notes": "Another note"
    },
    {
        "FirstName": "Bob",
        "LastName": "Williams",
        "FullName": "Bob Williams",
        "Email": "bob.williams@example.org",
        "EmployeeID": "EMP003",
        "Notes": "Private data"
    }
]

for i, record in enumerate(test_records, 1):
    print(f"\nRecord {i}:")
    print("-" * 80)
    
    anon_first = first_handler.anonymize(record["FirstName"])
    anon_last = last_handler.anonymize(record["LastName"])
    anon_full = full_handler.anonymize(record["FullName"])
    anon_email = email_handler.anonymize(record["Email"])
    anon_id = id_handler.anonymize(record["EmployeeID"])
    anon_misc = misc_handler.anonymize(record["Notes"])
    
    print(f"FirstName:   {record['FirstName']:20} → {anon_first}")
    print(f"LastName:    {record['LastName']:20} → {anon_last}")
    print(f"FullName:    {record['FullName']:20} → {anon_full}")
    print(f"Email:       {record['Email']:20} → {anon_email}")
    print(f"EmployeeID:  {record['EmployeeID']:20} → {anon_id}")
    print(f"Notes:       {record['Notes']:20} → '{anon_misc}'")
    
    expected_full = f"{anon_first} {anon_last}"
    expected_email_prefix = f"{anon_first.lower()}.{anon_last.lower()}"
    email_prefix = anon_email.split('@')[0] if '@' in anon_email else ""
    
    print(f"\n  ✓ FullName matches: {anon_full == expected_full}")
    print(f"  ✓ Email prefix matches: {email_prefix == expected_email_prefix}")

print("\n" + "=" * 80)
print("Testing Edge Cases")
print("=" * 80)

edge_cases = [
    ("None value", None),
    ("Empty string", ""),
    ("Single name", "Madonna"),
    ("Email without dot", "alice@example.com"),
    ("Email with underscore", "alice_johnson@company.com"),
]

for label, value in edge_cases:
    print(f"\n{label}: {value!r}")
    print(f"  FirstName: {first_handler.anonymize(value)!r}")
    print(f"  FullName:  {full_handler.anonymize(value)!r}")
    print(f"  Email:     {email_handler.anonymize(value)!r}")
    print(f"  ID:        {id_handler.anonymize(value)!r}")
    print(f"  Misc:      {misc_handler.anonymize(value)!r}")

print("\n" + "=" * 80)
print("Testing Determinism (same input → same output)")
print("=" * 80)

test_name = "TestName"
results = [first_handler.anonymize(test_name) for _ in range(5)]
print(f"Input: {test_name}")
print(f"Results: {results}")
print(f"✓ All identical: {len(set(results)) == 1}")

