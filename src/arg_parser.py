
import argparse

from src.enums import Mode


def argument_parser() -> tuple[str | Mode, str, str, str]:
    parser = argparse.ArgumentParser(description="Run on a file or directory with optional function")

    # mutually exclusive: -d OR -f
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-d",
        "--directory",
        help="Path to directory"
    )

    group.add_argument(
        "-f",
        "--file",
        help="Path to file"
    )

    # optional argument
    parser.add_argument(
        "-func",
        help="Optional function to run"
    )

    args = parser.parse_args()

    # handle input source
    target = args.directory if args.directory else args.file

    if args.directory:
        print(f"Mode: directory -> {target}")
    else:
        print(f"Mode: file -> {target}")

    # handle optional function
    if args.func:
        print(f"Function: {args.func}")
    else:
        print("No function specified")

    # TODO update
    search_dir = 'fake_real_tests/test_module_collector/tests'
    search_file = ''
    search_test_function = ''
    mode = 'NORMAL'
    
    return mode, search_dir, search_file, search_test_function
