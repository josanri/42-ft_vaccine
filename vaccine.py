import argparse

from src.sql_injection_injector import SQLInjector

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vaccine ./vaccine.py [-o output_file, -X method] URL')
    parser.add_argument('-o', '--output',
                        action='store',
                        help="specify archive file")
    parser.add_argument('-X',
                        action='store',
                        default='get',
                        const='get',
                        nargs='?',
                        choices=["get", "post"],
                        help="HTTP method for executing the sql injection")
    parser.add_argument('url',
                        action='store',
                        help="URL where injections will be done")
    args = parser.parse_args()
    SQLInjector(args.url, args.output, args.X).inject()