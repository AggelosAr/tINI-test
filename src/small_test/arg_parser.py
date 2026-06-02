from argparse import ArgumentParser

from small_test.enums import Mode


def receive_args() -> tuple[Mode, str, str, str]:
    parser = ArgumentParser(
        description='Small Test Framework'
    )

    #
    # Verbosity modes
    #
    verbosity = parser.add_mutually_exclusive_group()

    verbosity.add_argument(
        '-NORMAL',
        action='store_true',
        help='Normal output mode'
    )

    verbosity.add_argument(
        '-SORT',
        action='store_true',
        help='Sorted output mode'
    )

    verbosity.add_argument(
        '-MINIMAL',
        action='store_true',
        help='Minimal output mode'
    )

    verbosity.add_argument(
        '-MINIMAL_NO_STACK',
        action='store_true',
        help='Minimal output mode without stack traces'
    )

    verbosity.add_argument(
        '-SUPER_MINIMAL',
        action='store_true',
        help='Super Minimal output mode'
    )

    #
    # Search options
    #

    parser.add_argument(
        '-d',
        '--directory',
        help='Run all tests in a directory'
    )

    parser.add_argument(
        '-f',
        '--file',
        help='Run all tests in a file'
    )

    #
    # Specific test
    #
    parser.add_argument(
        '-t',
        '--test',
        help='Run a specific test function'
    )

    args = parser.parse_args()

    #
    # Mode
    #
    mode = Mode.NORMAL

    if args.SORT:
        mode = Mode.SORT
    elif args.MINIMAL:
        mode = Mode.MINIMAL
    elif args.MINIMAL_NO_STACK:
        mode = Mode.MINIMAL_NO_STACK
    elif args.SUPER_MINIMAL:
        mode = Mode.SUPER_MINIMAL

    #
    # Search targets
    #
    search_dir = args.directory or ''
    search_file = args.file or ''
    search_test_function = args.test or ''

    #
    # Default behavior:
    # search current directory
    #
    if not search_dir and not search_file and not search_test_function:
        search_dir = '.'

    return (
        mode,
        search_dir,
        search_file,
        search_test_function,
    )