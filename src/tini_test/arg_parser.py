from argparse import ArgumentParser, RawTextHelpFormatter
from typing import TypedDict

from tini_test.coverage.consts import METADATA_FILE
from tini_test.enums import Coverage, RunMode, Verbosity
from tini_test.misc.annotations import (DirectoryPath, FileName,
                                        TestFunctionName)


class CoreArgsDict(TypedDict):
    run_mode: RunMode
    verbosity: Verbosity

    coverage: Coverage
    coverage_target: DirectoryPath | FileName | None
    store_coverage_at: DirectoryPath | FileName | None

    search_dir: DirectoryPath
    file_name: FileName | None
    test_function: TestFunctionName | None


class CoverageMergeArgsDict(TypedDict):
    merge_directory: DirectoryPath | FileName | None


class CoverageGenerateReportArgsDict(TypedDict):
    source: DirectoryPath | FileName | None
    store: DirectoryPath | FileName | None


def receive_args() -> CoreArgsDict | CoverageMergeArgsDict | CoverageGenerateReportArgsDict:

    parser = ArgumentParser(
        description='tINI-test', formatter_class=RawTextHelpFormatter
    )


    # Search options
    parser.add_argument('-d',
                        '--directory',
                        default='.',
                        help=r'''
Run all tests in a directory, default is current directory.
                              ''')


    parser.add_argument('-f',
                        '--file',
                        help=r'''
Run all tests in a file.
                              ''')


    parser.add_argument('-t',
                        '--test',
                        help=r'''
Run a specific test function.
                              ''')


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

    # Coverage options
    parser.add_argument('--coverage',
                        action='store_const',
                        const=Coverage.ENABLED,
                        default=Coverage.DISABLED,
                        help=Coverage.arg_parser_info())


    parser.add_argument('--coverage-target',
                        default=None,
                        help=r'''
> This option can only be used when `--coverage` or `--coverage-generate-report` is enabled.
> Can be a single file or a directory.

Specify the target directory for coverage analysis.
All python file(s) in the target directory will be considered for coverage analysis.

* If no argument is provided, the current directory will be used.
* The path can be a relative or absolute path.
                              ''')


    parser.add_argument('--coverage-store',
                        default=None,
                        help=r'''
> This option can only be used when `--coverage` or `--coverage-generate-report` is enabled.

Specify the path where the coverage metadata will be stored.
If the path is specified as a file. It should follow the naming convention of the coverage metadata file.
e.g. `%s...`

* If no argument is provided, the current directory will be used.
* The path can be a relative or absolute path.
                              ''' % METADATA_FILE)


    # TODO add --keep ? 
    # TODO maybe also option for merge destination?
    parser.add_argument('--coverage-merge',
                        nargs='?',
                        const=True,
                        help=r'''
> This option can only be used alone. ( `--coverage-merge args` )
> If any other options are specified, they will be ignored.

Specify the directory containing coverage files to be merged into a single coverage metadata file.
As a result all files starting with `%s` in the specified directory will be considered for merging.
Creates a new merged coverage metadata file from all coverage metadata in the target directory.

* Does not modify the original coverage files.
* If no argument is provided, the current directory will be used.
* The path can be a relative or absolute path.
                              ''' % METADATA_FILE)


    parser.add_argument('--coverage-generate-report',
                        action='store_const',
                        const=True,
                        default=False,
                        help=r'''
> This option can only be used alone. ( `--coverage-generate-report` ) 
> Doesn't accept any arguments.
> Can only be used in combination with:

    1. --coverage-target ( source file(s) for analysis )
    2. --coverage-store  ( a single coverage metadata file )

> If any other options are specified, they will be ignored.

Helper option to generate a coverage HTML report from the merged coverage data.
It will parse the `%s` file and generate an HTML report based on its contents.

If no options are specified, the current directory will be used as the default location
for the source files and for the coverage metadata file.

* The path can be a relative or absolute path.
                              ''' % METADATA_FILE)


    args = parser.parse_args()

    if args.coverage_merge:
        return {
            'merge_directory': args.coverage_merge if not isinstance(args.coverage_merge, bool) else None
        }

    if args.coverage_generate_report:
        return {
            'source': args.coverage_target,
            'store': args.coverage_store,
        }

    if args.coverage == Coverage.DISABLED:
        if args.coverage_target or args.coverage_store:
            parser.error('--coverage-target and --coverage-store require --coverage.')

    return {
        'run_mode': args.run_mode,
        'verbosity': args.verbosity,

        'coverage': args.coverage,
        'coverage_target': args.coverage_target,
        'store_coverage_at': args.coverage_store,

        'search_dir': args.directory,
        'file_name': args.file,
        'test_function': args.test
    }
