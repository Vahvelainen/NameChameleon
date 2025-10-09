from anonymization.core.anonymizer import Anonymizer

column_config = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'FullName': 'full_name',
    'Email': 'email',
    'EmployeeID': 'id',
    'InternalNotes': 'misc'
}

anonymizer = Anonymizer(
    column_config=column_config,
    locale='en_US'
)

anonymizer.anonymize_excel('input.xlsx', 'output_anonymized.xlsx')

print(f"Anonymization complete!")
print(f"Salt (save this if you need reproducibility): {anonymizer.get_salt().hex()}")

