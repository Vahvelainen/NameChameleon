import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from anonymization.core.anonymizer import Anonymizer

print("=" * 80)
print("Creating Test Data")
print("=" * 80)

test_data = {
    'FirstName': ['John', 'Alice', 'Bob', 'Mary'],
    'LastName': ['Smith', 'Johnson', 'Williams', 'Brown'],
    'FullName': ['John Smith', 'Alice Johnson', 'Bob Williams', 'Mary Brown'],
    'Email': ['john.smith@company.com', 'alice.johnson@company.com', 'bob.williams@example.org', 'mary.brown@company.com'],
    'EmployeeID': ['EMP001', 'EMP002', 'EMP003', 'EMP004'],
    'Department': ['Engineering', 'Sales', 'Marketing', 'Engineering'],
    'Notes': ['Private info 1', 'Confidential 2', 'Secret 3', 'Internal 4']
}

df = pd.DataFrame(test_data)

df.to_csv('test_input.csv', index=False)
print("✓ Created test_input.csv")

with pd.ExcelWriter('test_input.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Employees', index=False)
    df.head(2).to_excel(writer, sheet_name='Summary', index=False)
print("✓ Created test_input.xlsx with 2 sheets")

print("\n" + "=" * 80)
print("Configuring Anonymizer")
print("=" * 80)

column_config = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'FullName': 'full_name',
    'Email': 'email',
    'EmployeeID': 'id',
    'Notes': 'misc'
}

anonymizer = Anonymizer(column_config=column_config, locale='en_US')
salt = anonymizer.get_salt()

print(f"Column config: {column_config}")
print(f"Salt: {salt.hex()[:32]}...")

print("\n" + "=" * 80)
print("Testing CSV Anonymization")
print("=" * 80)

anonymizer.anonymize_csv('test_input.csv', 'test_output.csv')
print("✓ Created test_output.csv")

original_df = pd.read_csv('test_input.csv')
anonymized_df = pd.read_csv('test_output.csv')

print("\nOriginal data (first 2 rows):")
print(original_df.head(2).to_string(index=False))

print("\nAnonymized data (first 2 rows):")
print(anonymized_df.head(2).to_string(index=False))

print("\nVerifications:")
print(f"  ✓ Row count preserved: {len(original_df)} → {len(anonymized_df)}")
print(f"  ✓ Department unchanged: {list(anonymized_df['Department']) == list(original_df['Department'])}")
print(f"  ✓ Notes deleted: {all(anonymized_df['Notes'] == '')}")
print(f"  ✓ All names changed: {not any(anonymized_df['FirstName'].isin(original_df['FirstName']))}")

print("\n" + "=" * 80)
print("Testing Excel Anonymization")
print("=" * 80)

anonymizer.anonymize_excel('test_input.xlsx', 'test_output.xlsx')
print("✓ Created test_output.xlsx")

excel_file = pd.ExcelFile('test_output.xlsx')
print(f"✓ Sheet names preserved: {excel_file.sheet_names}")

employees_df = pd.read_excel('test_output.xlsx', sheet_name='Employees')
summary_df = pd.read_excel('test_output.xlsx', sheet_name='Summary')

print(f"✓ Employees sheet: {len(employees_df)} rows")
print(f"✓ Summary sheet: {len(summary_df)} rows")

print("\n" + "=" * 80)
print("Testing Name Consistency")
print("=" * 80)

for idx, row in anonymized_df.iterrows():
    first = row['FirstName']
    last = row['LastName']
    full = row['FullName']
    email = row['Email']
    
    expected_full = f"{first} {last}"
    expected_email_prefix = f"{first.lower()}.{last.lower()}"
    email_prefix = email.split('@')[0] if '@' in email else ""
    
    print(f"Row {idx+1}:")
    print(f"  Name: {first} {last}")
    print(f"  FullName matches: {full == expected_full}")
    print(f"  Email prefix matches: {email_prefix == expected_email_prefix}")
    
    if full != expected_full or email_prefix != expected_email_prefix:
        print(f"  ❌ MISMATCH!")
        print(f"     Full: expected '{expected_full}', got '{full}'")
        print(f"     Email: expected '{expected_email_prefix}@...', got '{email}'")

print("\n" + "=" * 80)
print("Testing Determinism with Same Salt")
print("=" * 80)

anonymizer2 = Anonymizer(column_config=column_config, salt=salt, locale='en_US')
anonymizer2.anonymize_csv('test_input.csv', 'test_output2.csv')

df1 = pd.read_csv('test_output.csv')
df2 = pd.read_csv('test_output2.csv')

all_match = df1.equals(df2)
print(f"✓ Results identical with same salt: {all_match}")

if not all_match:
    print("Differences found:")
    for col in df1.columns:
        if not df1[col].equals(df2[col]):
            print(f"  Column '{col}' differs")

print("\n" + "=" * 80)
print("All tests completed!")
print("=" * 80)

