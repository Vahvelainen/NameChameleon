from anonymization import Anonymizer

# Define which columns to anonymize and their types
column_config = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'FullName': 'full_name',
    'Email': 'email',
    'EmployeeID': 'id',
    'InternalNotes': 'misc'
}

# Create anonymizer instance
anonymizer = Anonymizer(
    column_config=column_config,
    locale='en_US'
)

# Anonymize the Excel file
anonymizer.anonymize_excel('input.xlsx', 'output_anonymized.xlsx')

print("Anonymization complete!")
print(f"Salt (save this if you need reproducibility): {anonymizer.get_salt().hex()}")

