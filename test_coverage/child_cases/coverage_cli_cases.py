import json
import os
import shutil
import subprocess
import sys
import tempfile

from tini_test import Shared, Test, WillRaise, must_equal, var
from tini_test.__main__ import _tini_test
from tini_test.arg_parser import receive_args
from tini_test.coverage._coverage import CoverageTracker
from tini_test.coverage.consts import METADATA_FILE, STORE

# This file is not a test file by itself. test_coverage_cli.py copies it into a
# generated test dir and runs tini_test on it in a subprocess, with coverage enabled.

MERGED = '%s_merged' % METADATA_FILE
STORE_NAME = '%s_merged' % METADATA_FILE

PKG_A = '''import os
x = dict(
    a=1,
    b=2,
)
def f():
    return 1
'''

PKG_B = 'y = 1\n'
PKG_C = 'z = 1\n'

EXPECTED = {'/x.py': {1, 2, 3}, '/y.py': {5}}


def _cli(args: list[str], cwd: str | None = None) -> dict:
    # Same code path as `python -m tini_test <args>`, but traced.
    old_argv, old_cwd = sys.argv, os.getcwd()
    try:
        if cwd:
            os.chdir(cwd)
        sys.argv = ['tini_test', *args]

        kwargs = receive_args()
        _tini_test(kwargs)
        return dict(kwargs)
    finally:
        sys.argv = old_argv
        os.chdir(old_cwd)


def _write_store(directory: str, name: str, data: dict[str, list[int]]) -> str:
    path = os.path.join(directory, name)
    with open(path, 'w') as f:
        json.dump(data, f)
    return path


def _read_store(path: str) -> dict[str, set[int]]:
    with open(path, 'r') as f:
        return {file: set(lines) for file, lines in json.load(f).items()}


def _merged_files(directory: str) -> list[str]:
    return sorted(f for f in os.listdir(directory) if f.startswith(MERGED))


def _populate(directory: str) -> None:
    _write_store(directory, '%s_a' % METADATA_FILE, {'/x.py': [1, 2], '/y.py': [5]})
    _write_store(directory, '%s_b' % METADATA_FILE, {'/x.py': [2, 3]})


def _make_dir() -> None:
    var.root = tempfile.mkdtemp(prefix='tini_test_merge_')


def _make_project() -> None:
    # root/
    #   .coverage_merged
    #   src/pkg_a.py
    #   src/sub/pkg_b.py
    #   other/pkg_c.py
    root = os.path.realpath(tempfile.mkdtemp(prefix='tini_test_report_'))

    for relative, content in (('src/pkg_a.py', PKG_A),
                              ('src/sub/pkg_b.py', PKG_B),
                              ('other/pkg_c.py', PKG_C)):
        path = os.path.join(root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    # Only the first line of the multi line statement was reported at runtime.
    with open(os.path.join(root, STORE_NAME), 'w') as f:
        json.dump({os.path.join(root, 'src/pkg_a.py'): [2]}, f)

    var.root = root


def _tracker(source: str | None, store: str | None) -> CoverageTracker:
    tracker = CoverageTracker.init_from_store(source=source, store=store)
    tracker.collect_files_from_source()
    return tracker


def _index(root: str) -> str:
    with open(os.path.join(root, STORE, 'index.html'), 'r') as f:
        return f.read()


# --coverage-merge

@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeWithOtherOptionsRunsOnlyMerge() -> None:
    root = var.root
    _populate(root)

    kwargs = _cli(['--coverage-merge', root, '-f', 'x'], cwd=root)

    # The other options are dropped, so the tests are never run.
    must_equal({'merge_directory': root}, kwargs)
    must_equal([MERGED], _merged_files(root))
    must_equal(EXPECTED, _read_store(os.path.join(root, MERGED)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeUsedAloneDefaultsToCurrentDirectory() -> None:
    root = var.root
    _populate(root)

    kwargs = _cli(['--coverage-merge'], cwd=root)

    must_equal({'merge_directory': None}, kwargs)
    must_equal([MERGED], _merged_files(root))
    must_equal(EXPECTED, _read_store(os.path.join(root, MERGED)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeRelativePath() -> None:
    root = var.root
    sub = os.path.join(root, 'sub')
    os.makedirs(sub)
    _populate(sub)

    _cli(['--coverage-merge', 'sub'], cwd=root)

    must_equal([MERGED], _merged_files(sub))
    must_equal([], _merged_files(root))
    must_equal(EXPECTED, _read_store(os.path.join(sub, MERGED)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeAbsolutePath() -> None:
    root = var.root
    _populate(root)

    # The working directory is somewhere else.
    _cli(['--coverage-merge', root])

    must_equal([MERGED], _merged_files(root))
    must_equal(EXPECTED, _read_store(os.path.join(root, MERGED)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeDoesNotModifyOriginalsOrOverwriteMerged() -> None:
    root = var.root
    _populate(root)

    CoverageTracker.merge(root)
    CoverageTracker.merge(root)

    must_equal([MERGED, '%s_0' % MERGED], _merged_files(root))

    must_equal({'/x.py': {1, 2}, '/y.py': {5}}, _read_store(os.path.join(root, '%s_a' % METADATA_FILE)))
    must_equal({'/x.py': {2, 3}}, _read_store(os.path.join(root, '%s_b' % METADATA_FILE)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeSkipsUnrelatedAndBrokenFiles() -> None:
    root = var.root
    _populate(root)

    with open(os.path.join(root, 'notes.txt'), 'w') as f:
        f.write('not a coverage file')

    with open(os.path.join(root, '%s_broken' % METADATA_FILE), 'w') as f:
        f.write('{not json')

    CoverageTracker.merge(root)

    must_equal(EXPECTED, _read_store(os.path.join(root, MERGED)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeNestedDirectories() -> None:
    root = var.root
    nested = os.path.join(root, 'a', 'b')
    os.makedirs(nested)
    _write_store(root, '%s_top' % METADATA_FILE, {'/x.py': [1]})
    _write_store(nested, '%s_nested' % METADATA_FILE, {'/x.py': [2]})

    CoverageTracker.merge(root)

    must_equal({'/x.py': {1, 2}}, _read_store(os.path.join(root, MERGED)))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeNonExistingAbsolutePath() -> None:
    root = var.root
    missing = os.path.join(root, 'missing')

    with WillRaise(FileNotFoundError):
        _cli(['--coverage-merge', missing])

    must_equal(False, os.path.exists(missing))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeNonExistingRelativePath() -> None:
    root = var.root

    with WillRaise(FileNotFoundError):
        _cli(['--coverage-merge', 'missing'], cwd=root)

    must_equal(False, os.path.exists(os.path.join(root, 'missing')))


@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_MergeFilePath() -> None:
    root = var.root
    store = _write_store(root, '%s_a' % METADATA_FILE, {'/x.py': [1]})

    with WillRaise(NotADirectoryError):
        _cli(['--coverage-merge', store])

    must_equal([], _merged_files(root))


# --coverage-generate-report

@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportWithOtherOptionsRunsOnlyReport() -> None:
    root = var.root

    kwargs = _cli(['--coverage-generate-report',
                   '--coverage-target', 'src',
                   '--coverage-store', STORE_NAME,
                   '-f', 'x'], cwd=root)

    # The other options are dropped, so the tests are never run.
    must_equal({'source': 'src', 'store': STORE_NAME}, kwargs)
    must_equal(True, os.path.isfile(os.path.join(root, STORE, 'index.html')))


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportTargetOmittedUsesCurrentDirectory() -> None:
    root = var.root

    kwargs = _cli(['--coverage-generate-report'], cwd=root)

    must_equal({'source': None, 'store': None}, kwargs)

    index = _index(root)
    must_equal(True, 'pkg_a.py' in index)
    must_equal(True, 'pkg_b.py' in index)
    must_equal(True, 'pkg_c.py' in index)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportRelativeTarget() -> None:
    root = var.root

    _cli(['--coverage-generate-report', '--coverage-target', 'src'], cwd=root)

    index = _index(root)
    must_equal(True, 'pkg_a.py' in index)
    must_equal(True, 'pkg_b.py' in index)
    must_equal(False, 'pkg_c.py' in index)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportRelativeTargetAndRelativeStore() -> None:
    root = var.root

    _cli(['--coverage-generate-report',
          '--coverage-target', 'other',
          '--coverage-store', STORE_NAME], cwd=root)

    index = _index(root)
    must_equal(False, 'pkg_a.py' in index)
    must_equal(True, 'pkg_c.py' in index)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportAbsoluteTargetAndStore() -> None:
    root = var.root

    # The report is written to the working directory, so use the project as that.
    _cli(['--coverage-generate-report',
          '--coverage-target', os.path.join(root, 'src'),
          '--coverage-store', os.path.join(root, STORE_NAME)], cwd=root)

    index = _index(root)
    must_equal(True, 'pkg_a.py' in index)
    must_equal(False, 'pkg_c.py' in index)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportCollectsCorrectFiles() -> None:
    root = var.root

    tracker = _tracker(os.path.join(root, 'src'), os.path.join(root, STORE_NAME))

    must_equal({os.path.join(root, 'src/pkg_a.py'), os.path.join(root, 'src/sub/pkg_b.py')},
               set(tracker.files))


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportSingleFileTarget() -> None:
    root = var.root
    pkg_a = os.path.join(root, 'src/pkg_a.py')

    tracker = _tracker(pkg_a, os.path.join(root, STORE_NAME))

    must_equal({pkg_a}, set(tracker.files))


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportNonExistingTargetCollectsNothing() -> None:
    root = var.root

    tracker = _tracker(os.path.join(root, 'missing'), os.path.join(root, STORE_NAME))

    must_equal({}, tracker.files)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportCountsMultiLineStatementOnce() -> None:
    root = var.root
    pkg_a = os.path.join(root, 'src/pkg_a.py')

    coverage = _tracker(pkg_a, os.path.join(root, STORE_NAME)).files[pkg_a]

    # import, x = dict(...), def f(), return 1
    must_equal(4, coverage.total_statements)
    # `import` and `def` are top level so they ran on import, `x` was hit on its first line.
    must_equal(3, coverage.covered_statements)
    must_equal(1, coverage.missing_statements)
    must_equal(75.0, coverage.score)

    # Every line of the multi line statement shares the status of its first line.
    must_equal(['run', 'run', 'run', 'run'], [str(coverage.lines[n].status) for n in (2, 3, 4, 5)])
    must_equal([False, True, True, True], [coverage.lines[n].is_continuation for n in (2, 3, 4, 5)])
    must_equal('missing', str(coverage.lines[7].status))


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportNonExistingStore() -> None:
    root = var.root

    with WillRaise(FileNotFoundError):
        _cli(['--coverage-generate-report',
              '--coverage-store', '%s_missing' % METADATA_FILE], cwd=root)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportStoreMustFollowNamingConvention() -> None:
    root = var.root

    with WillRaise(ValueError):
        _cli(['--coverage-generate-report',
              '--coverage-store', os.path.join(root, 'src/pkg_a.py')], cwd=root)


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_GenerateReportNoStoreInCurrentDirectory() -> None:
    root = var.root
    empty = os.path.join(root, 'empty')
    os.makedirs(empty)

    with WillRaise(FileNotFoundError):
        _cli(['--coverage-generate-report'], cwd=empty)


# Smoke tests: the real entry point, as a user would run it.
# They are not traced since they run in yet another process.

@Shared(var.root)
@Test.case(_make_dir, lambda: shutil.rmtree(var.root))
def test_SmokeMergeEntryPoint() -> None:
    root = var.root
    _populate(root)

    completed_process = subprocess.run([sys.executable, '-m', 'tini_test', '--coverage-merge'],
                                       cwd=root, timeout=10, text=True, capture_output=True)

    must_equal(0, completed_process.returncode)
    must_equal(True, 'coverage metadata saved to' in completed_process.stdout)
    must_equal([MERGED], _merged_files(root))


@Shared(var.root)
@Test.case(_make_project, lambda: shutil.rmtree(var.root))
def test_SmokeGenerateReportEntryPoint() -> None:
    root = var.root

    completed_process = subprocess.run([sys.executable, '-m', 'tini_test', '--coverage-generate-report'],
                                       cwd=root, timeout=10, text=True, capture_output=True)

    must_equal(0, completed_process.returncode)
    must_equal(True, 'Coverage report generated' in completed_process.stdout)
    must_equal(True, os.path.isfile(os.path.join(root, STORE, 'index.html')))
