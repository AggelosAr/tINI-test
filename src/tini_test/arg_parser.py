from argparse import ArgumentParser, RawTextHelpFormatter
from typing import NotRequired, TypedDict

from tini_test.misc.annotations import (DirectoryPath, FileName,
                                        TestFunctionName)

from .enums import RunMode, Verbosity


class ArgsDict(TypedDict):
    run_mode: RunMode
    verbosity: Verbosity
    search_dir: DirectoryPath
    file_name: NotRequired[FileName | None]
    test_function: NotRequired[TestFunctionName | None]
    

def receive_args() -> ArgsDict:

    parser = ArgumentParser(
        description='Small Test Framework', formatter_class=RawTextHelpFormatter
    )

    # Verbosity options
    parser.add_argument('-v',
                        '--verbosity',
                        type=Verbosity.arg_parser_type,
                        default=Verbosity.SORT,
                        help=(Verbosity.supported_modes_help_msg()
                              +
                              Verbosity.arg_parser_info()))

    # Run options
    parser.add_argument('-r',
                        '--run-mode',
                        type=RunMode.arg_parser_type,
                        default=RunMode.SYNC,
                        help=(RunMode.supported_modes_help_msg()
                              +
                              RunMode.arg_parser_info()))
    
    # Search options
    parser.add_argument('-d',
                        '--directory',
                        default='.',
                        help='Run all tests in a directory, default is current directory')

    parser.add_argument('-f',
                        '--file',
                        help='Run all tests in a file')

    parser.add_argument('-t',
                        '--test',
                        help='Run a specific test function')

    args = parser.parse_args()

    return {'run_mode': args.run_mode,
            'verbosity': args.verbosity,
            'search_dir': args.directory,
            'file_name': args.file,
            'test_function': args.test}
