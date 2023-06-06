import argparse

from src.sql_injection_injector import SQLInjector

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vaccine ./vaccine.py [-o output_file, -X method]')
    parser.add_argument('-o', '--output',
                        action='store',
                        help="specify archive file")
    parser.add_argument('-X',
                        action='store',
                        default='GET',
                        const='GET',
                        nargs='?',
                        choices=["GET", "POST", "PUT", "DELETE"],
                        help="HTTP method for executing the sql injection")
    args = parser.parse_args()
    SQLInjector(args.output, args.X)