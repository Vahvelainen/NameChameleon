import sys
from pathlib import Path
from argparse import Namespace
import pandas as pd

from anonymization.core.anonymizer import Anonymizer
from anonymization.cli.helpers import detect_file_columns, interactive_column_mapping, load_config_file


def show_columns_command(file_path: str) -> None:
    path = Path(file_path)
    
    if path.suffix.lower() == '.csv':
        columns = detect_file_columns(file_path)
        print(f"\nColumns in '{file_path}':")
        for i, col in enumerate(columns, 1):
            print(f"  {i}. {col}")
    elif path.suffix.lower() in ['.xlsx', '.xls']:
        xl = pd.ExcelFile(file_path)
        print(f"\nColumns in '{file_path}':")
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=0)
            print(f"\n  Sheet: {sheet_name}")
            for i, col in enumerate(df.columns, 1):
                print(f"    {i}. {col}")
        
        print(f"\n  Unique columns across all sheets:")
        unique_cols = detect_file_columns(file_path)
        for i, col in enumerate(unique_cols, 1):
            print(f"    {i}. {col}")
    
    print()


def anonymize_command(args: Namespace) -> None:
    column_config = {}
    
    if args.config:
        column_config = load_config_file(args.config)
        print(f"Loaded configuration from: {args.config}")
    elif args.interactive:
        input_path = Path(args.input)
        if input_path.suffix.lower() in ['.xlsx', '.xls']:
            print("\nDetecting unique columns across all Excel sheets...")
            print("(The configuration will apply to all sheets)")
        
        columns = detect_file_columns(args.input)
        column_config = interactive_column_mapping(columns)
    else:
        print("Error: Must specify either --config or --interactive")
        sys.exit(1)
    
    if not column_config:
        print("No columns configured for anonymization. Exiting.")
        sys.exit(1)
    
    print(f"\nColumn configuration:")
    for col, col_type in column_config.items():
        print(f"  {col} -> {col_type}")
    
    salt = bytes.fromhex(args.salt) if args.salt else None
    
    anonymizer = Anonymizer(
        column_config=column_config,
        salt=salt,
        locale=args.locale
    )
    
    input_path = Path(args.input)
    if input_path.suffix.lower() == '.csv':
        anonymizer.anonymize_csv(args.input, args.output)
    elif input_path.suffix.lower() in ['.xlsx', '.xls']:
        anonymizer.anonymize_excel(args.input, args.output)
    else:
        print(f"Error: Unsupported file format: {input_path.suffix}")
        sys.exit(1)
    
    print(f"\n✓ Anonymized file saved to: {args.output}")
    
    if args.show_salt:
        salt_hex = anonymizer.get_salt().hex()
        print(f"\nSalt (save for reproducibility): {salt_hex}")

