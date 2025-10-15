import argparse
import sys

from anonymization.cli.commands import AnonymizeCommand, ShowColumnsCommand


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='chameleon',
        description='Anonymize CSV and Excel files with deterministic pseudonymization'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    anonymize_parser = subparsers.add_parser('anonymize', help='Anonymize a file')
    anonymize_parser.add_argument('input', help='Input file path (CSV or Excel)')
    anonymize_parser.add_argument('output', help='Output file path')
    anonymize_parser.add_argument(
        '-c', '--config',
        help='JSON config file with column mappings'
    )
    anonymize_parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interactive mode: select column types manually'
    )
    anonymize_parser.add_argument(
        '--salt',
        help='Salt as hex string for reproducible anonymization'
    )
    anonymize_parser.add_argument(
        '--locale',
        default='en_US',
        help='Locale for name generation (default: en_US)'
    )
    anonymize_parser.add_argument(
        '--show-salt',
        action='store_true',
        help='Display the salt after anonymization'
    )
    
    columns_parser = subparsers.add_parser('columns', help='Show columns in a file')
    columns_parser.add_argument('input', help='Input file path (CSV or Excel)')
    
    args = parser.parse_args()
    
    if args.command == 'anonymize':
        command = AnonymizeCommand(
            input_path=args.input,
            output_path=args.output,
            config_path=args.config,
            interactive=args.interactive,
            salt=args.salt,
            locale=args.locale,
            show_salt=args.show_salt
        )
        command.execute()
    elif args.command == 'columns':
        command = ShowColumnsCommand(args.input)
        command.execute()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

