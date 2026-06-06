from argparse import ArgumentParser
from typing import Optional

from tini_test.misc.annotations import Directory, FileName, TestFunctionName

from .enums import RunMode, Verbosity


def receive_args() -> tuple[RunMode,
                            Verbosity,
                            Directory,
                            Optional[FileName],
                            Optional[TestFunctionName]]:
    
    parser = ArgumentParser(
        description='Small Test Framework'
    )

    # Verbosity options
    parser.add_argument('-v',
                        '--verbosity',
                        type=Verbosity.arg_parser_type,
                        default=Verbosity.SORT,
                        help=Verbosity.supported_modes_help_msg())

    # Run options
    parser.add_argument('-r',
                        '--run-mode',
                        type=RunMode.arg_parser_type,
                        default=RunMode.SYNC,
                        help=RunMode.supported_modes_help_msg())
    
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

    return (args.run_mode,
            args.verbosity,
            args.directory,
            args.file,
            args.test)
