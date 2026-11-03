from __future__ import annotations

import html
import io
import json
import os
import shutil
import tokenize
from collections import Counter
from datetime import datetime
from functools import cached_property, partial
from pathlib import Path
from types import FrameType
from typing import Optional

from tini_test._internals._ast_utils import AstParser
from tini_test._internals.consts import _V2_COVERAGE
from tini_test.coverage.consts import (_TOGGLE_SCRIPT, ASSERT_NOT_COVERED,
                                       EXCLUDED_MARKER, METADATA_FILE, STORE,
                                       STYLE_FILE, SVG_FILE)
from tini_test.coverage.enums import HTMLNodeType, LineStatus
from tini_test.coverage.html import HTMLHyperLink, HTMLNode, HTMLTemplate
from tini_test.enums import Color, ScoreClass
from tini_test.misc.annotations import (CodeLineNumber, CoverageStore,
                                        DirectoryPath, DocstringId, FileName,
                                        LineContent, Offset, StatementId,
                                        StrippedLineContent)
from tini_test.misc.exceptions import (CoverageDeserializationError,
                                       CoverageDeserializationFileContentError,
                                       CoverageDeserializationFileNameError,
                                       CoverageRequestedForInvalidFile,
                                       TiniTestInternalException)


class InlineComment:

    def __init__(self, _start: int) -> None:
        self.start = _start

    @classmethod
    def assert_not_covered(cls, 
                           line_content: LineContent, 
                           inline_comment: InlineComment | None) -> bool:
        '''
        >>> # >>> assert missing

        If a line has the < ASSERT_NOT_COVERED > marker. We must assert 
        that it correctly is < MISSING > and < NOT_COVERED > in the opposite case.

        >>> e.g. we want it to not be covered at runtime.
        '''
        if inline_comment is None:
            return False
        
        return line_content[inline_comment.start:].strip() == ASSERT_NOT_COVERED
    
    @classmethod
    def from_file_read(cls, source: str) -> dict[CodeLineNumber, InlineComment]:
        comments = {}

        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
       
        for token in tokens:
            if token.type != tokenize.COMMENT:
                continue

            line_number = token.start[0]  # 1-based
            comment_start = token.start[1]

            comments[line_number] = InlineComment(comment_start)

        return comments



class Line:

    def __init__(self, 
                 line_number: CodeLineNumber, 
                 line_content: LineContent, 
                 status: LineStatus,
                 is_continuation: Optional[bool] = False,
                 inline_comment: Optional[InlineComment] = None) -> None:
        self.line_number = line_number
        self.line_content = line_content
        self.status = status
        # Not the first line of a multi line statement.
        self.is_continuation = is_continuation

        self.inline_comment = inline_comment

    @cached_property
    def sline(self) -> StrippedLineContent:
        return self.line_content.strip()
    
    @property
    def is_inline_commented(self) -> bool:
        return self.inline_comment is not None

    @property
    def is_ellipsis(self) -> bool:
        return self.sline == '...'

    @property
    def is_comment(self) -> bool:
        return self.sline.startswith('#')

    @property
    def is_empty(self) -> bool:
        return self.sline is str()
    
    @property
    def is_else_or_finally(self) -> bool:
        if self.sline.startswith('else:'):
            return True

        if self.sline.startswith('finally:'):
            return True

        return False
    
    def add_inline_comment(self, inline_comment: InlineComment) -> None:
        self.inline_comment = inline_comment

    def get_split_line(self) -> tuple[str, str]:
        if self.inline_comment:
            _code = self.line_content[:self.inline_comment.start]
            comment = self.line_content[self.inline_comment.start:]
            return _code, comment
        return self.line_content, ''


class FileCoverage:
    # Maybe split it into functions class for better modularity
    def __init__(self, 
                 file_path: Path, 
                 runtime_covered_lines: set[CodeLineNumber],
                 autocomplete_top_levels: bool) -> None:
        self.href = ''

        self.file_path = file_path
        self.lines: dict[CodeLineNumber, Line] = {}

        self._statement_counts: Counter[LineStatus] = Counter()
        
        self._source = ''

        self._autocomplete_top_levels = autocomplete_top_levels
        if 0 in runtime_covered_lines:
            self._autocomplete_top_levels = True

        runtime_covered_lines.discard(0)

        self.runtime_covered_lines = runtime_covered_lines

    @cached_property
    def parser(self) -> AstParser:
        return AstParser.from_file_read(self.source, str(self.file_path))

    @cached_property
    def line_to_statement(self) -> dict[CodeLineNumber, StatementId]:
        return self.parser.extract_line_to_statement()

    @cached_property
    def statement_to_lines(self) -> dict[StatementId, set[CodeLineNumber]]:
        return self.group_by_category(self.line_to_statement)

    @cached_property
    def line_to_docstring(self) -> dict[CodeLineNumber, DocstringId]:
        return self.parser.extract_line_to_docstring()

    @cached_property
    def docstring_to_lines(self) -> dict[DocstringId, set[CodeLineNumber]]:
        return self.group_by_category(self.line_to_docstring)
    
    @cached_property
    def inline_comments(self) -> dict[CodeLineNumber, InlineComment]:
        return InlineComment.from_file_read(self.source)

    @cached_property
    def raw_lines(self) -> list[str]:
        return self.source.splitlines()
    
    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, value: str) -> None:
        self._source = value
   
    @property
    def top_levels(self) -> list[CodeLineNumber]:
        # Important: the requested root dir we consider source 
        # May exist but there may not be any lines covered yet.
        # If the path exists in the store, we will automplete top levels.
        # Since coverege is now implemented on the import level as well
        # It would be better if the <add_top_levels> is removed all together.
        if not self._autocomplete_top_levels:
            return []
        
        return self.parser.extract_top_level_lines()
    
    @property
    def total_statements(self) -> int:
        return len(self.statement_to_lines)

    @property
    def covered_statements(self) -> int:
        return self._statement_counts[LineStatus.RUN]

    @property
    def _X_correctly_missing_statements(self) -> int:
        return self._statement_counts[LineStatus.CORRECTLY_MISSING]
    
    @property
    def missing_statements(self) -> int:
        return self._statement_counts[LineStatus.MISSING]

    @property
    def _X_incorrectly_covered_statements(self) -> int:
        return self._statement_counts[LineStatus.INCORRECTLY_RUN]
    
    @property
    def excluded_statements(self) -> int:
        return self._statement_counts[LineStatus.EXCLUDED]

    @property
    def comment_lines(self) -> int:
        # comment are lines 
        return self._statement_counts[LineStatus.COMMENT]

    @property
    def docstring_lines(self) -> int:
        return self._statement_counts[LineStatus.DOCSTRING]

    @property
    def empty_lines(self) -> int:
        # empty are lines 
        return self._statement_counts[LineStatus.EMPTY]

    @property
    def score(self) -> float:
        run, missing = self.covered_statements, self.missing_statements

        run += self._X_correctly_missing_statements
        missing += self._X_incorrectly_covered_statements

        total = run + missing
        return 100.0 * run / total if total else 100.0

    def group_by_category(self, category: dict[CodeLineNumber, int]) -> dict[int, set[CodeLineNumber]]:
        result: dict[int, set[CodeLineNumber]] = {}
        
        for item, lines in category.items():
            result.setdefault(lines, set()).add(item)

        return result

    def get_python_statement(self, line: CodeLineNumber) -> set[CodeLineNumber]:
        _id = self.line_to_statement.get(line, -1)
        return self.statement_to_lines.get(_id, set())

    def get_docstring(self, line: CodeLineNumber) -> set[CodeLineNumber]:
        _id = self.line_to_docstring.get(line, -1)
        return self.docstring_to_lines.get(_id, set())
    
    # TODO add exclude as an option to statements.
    def handle_excluded_file(self) -> bool:
        lines = self.raw_lines

        if lines and lines[0].startswith(EXCLUDED_MARKER):

            for l_no, l_cont in enumerate(lines, start=1):
                self.lines[l_no] = Line(l_no, l_cont, LineStatus.EXCLUDED)
                self._statement_counts[LineStatus.EXCLUDED] += 1

            self.statement_to_lines.clear()
            return True
        
        return False

    def handle_empty_line(self, line: Line):
        line.is_continuation = False
        line.status = LineStatus.EMPTY
        self._statement_counts[LineStatus.EMPTY] += 1

    def handle_comment(self, line: Line):
        line.is_continuation = False
        line.status = LineStatus.COMMENT
        self._statement_counts[LineStatus.COMMENT] += 1

    def handle_ellipsis(self, line: Line):
        line.status = LineStatus.EXCLUDED
        # Comments are allowed on ellipsis
        inline_comment = self.inline_comments.get(line.line_number)
        if inline_comment:
            line.add_inline_comment(inline_comment)
            self._statement_counts[LineStatus.COMMENT] += 1

        match line.line_number in self.runtime_covered_lines:
            # Ellispis sometimes are counted as < MISSING > statements
            # and other times as < RUN >
            case True:
                self._statement_counts[LineStatus.RUN] -= 1

            case False:
                self._statement_counts[LineStatus.MISSING] -= 1

        self._statement_counts[LineStatus.EXCLUDED] += 1

    def clean_up_else_or_finally(self, line: Line):
        # Else/finally blocks are skipped @extract_line_to_statement
        line.status = LineStatus.EXCLUDED
        self._statement_counts[LineStatus.EXCLUDED] += 1

        inline_comment = self.inline_comments.get(line.line_number)

        if inline_comment:
            line.add_inline_comment(inline_comment)
            self._statement_counts[LineStatus.COMMENT] += 1

    def handle_docstring(self, l_nos: list[CodeLineNumber]) -> None:
        self._statement_counts[LineStatus.DOCSTRING] += 1

        for l_no in l_nos:
            line = Line(l_no, self.raw_lines[l_no - 1], LineStatus.DOCSTRING)
            self.lines[l_no] = line

        # Comments are allowed at the end of the docstring
        # Or if the docstring is in-line.
        inline_comment = self.inline_comments.get(l_nos[-1])
        if inline_comment:
            self.lines[l_nos[-1]].add_inline_comment(inline_comment)
            self._statement_counts[LineStatus.COMMENT] += 1

    def python_handle_inline_comment(self, line: Line) -> bool:
        assert_not_covered = False

        inline_comment = self.inline_comments.get(line.line_number)

        if inline_comment is None:
            return assert_not_covered

        line.is_continuation = False
        line.add_inline_comment(inline_comment)
        self._statement_counts[LineStatus.COMMENT] += 1

        _assert_not_covered = InlineComment.assert_not_covered

        return _assert_not_covered(line.line_content, inline_comment)
    
    def handle_python_statement(self, l_nos: list[CodeLineNumber]) -> None:
        # Assume that for some reason we get missing information
        # In a multi-line statement, we may get only a single line as < RUN > ?
        statuses = []

        assert_not_covered = False

        for l_no in range(l_nos[0], l_nos[-1] + 1):
            line = Line(l_no, self.raw_lines[l_no - 1], LineStatus.NULL)
            line.is_continuation = True
            
            self.lines[l_no] = line
            
            # Handle empty line
            if line.is_empty:
                self.handle_empty_line(line)

            # Handle comment line
            if line.is_comment or self.inline_comments.get(line.line_number):
                res = self.python_handle_inline_comment(line)
                assert_not_covered |= res

            if line.is_ellipsis:
                self.handle_ellipsis(line)

            match l_no in self.runtime_covered_lines:
                case True:
                    statuses.append(LineStatus.RUN)
                case False:
                    statuses.append(LineStatus.MISSING)

        status = LineStatus.RUN if any(s == LineStatus.RUN for s in statuses) else LineStatus.MISSING

        if assert_not_covered:

            match status:
                case LineStatus.RUN:
                    status = LineStatus.INCORRECTLY_RUN

                case LineStatus.MISSING:
                    status = LineStatus.CORRECTLY_MISSING

        # Flag the first line of the statement as not a continuation
        self.lines[l_nos[0]].is_continuation = False
        self._statement_counts[status] += 1

        for l_no in range(l_nos[0], l_nos[-1] + 1):

            line = self.lines[l_no]

            if line.is_empty:
                line.status = LineStatus.EMPTY
                line.is_continuation = False
                continue

            if line.is_comment:
                line.status = LineStatus.COMMENT
                line.is_continuation = False
                continue

            if line.is_ellipsis:
                if line.status == LineStatus.MISSING:
                    line.status = LineStatus.EXCLUDED
                line.is_continuation = False
                continue

            line.status = status

    def handle_statement_or_docstring(self, l_no: CodeLineNumber) -> Offset:
        _offset = 0

        l_nos = self.get_python_statement(l_no)
        if l_no in l_nos:
            _offset += len(l_nos)
            self.handle_python_statement(list(sorted(l_nos)))
            return _offset

        l_nos = self.get_docstring(l_no)
        if l_no in l_nos:
            _offset += len(l_nos)
            self.handle_docstring(list(sorted(l_nos)))
            return _offset
        
        return _offset

    def handle_single_python_line(self, l_no: CodeLineNumber) -> Offset:
        line = Line(l_no, self.raw_lines[l_no - 1], LineStatus.MISSING)
        self.lines[l_no] = line
        _offset = 0

        if line.is_empty:
            _offset += 1
            self.handle_empty_line(line)
            return _offset
        
        if line.is_comment:
            _offset += 1
            self.handle_comment(line)
            return _offset

        if line.is_ellipsis:
            _offset += 1
            self.handle_ellipsis(line)
            return _offset

        if line.is_else_or_finally:
            _offset += 1
            self.clean_up_else_or_finally(line)
            return _offset

        return _offset

    def iterate_python_file(self) -> None:
        l_no = 1

        while l_no < len(self.raw_lines) + 1:

            offset = self.handle_statement_or_docstring(l_no)

            if not offset:
                offset = self.handle_single_python_line(l_no)

            assert offset, TiniTestInternalException(LineStatus)
            l_no += offset

    def parse_file(self) -> None:
        with open(self.file_path, 'r') as f:
            self.source = f.read()

        self.runtime_covered_lines.update(self.top_levels)

        if self.handle_excluded_file():
            return

        self.iterate_python_file()

    def set_href(self, href: str) -> None:
        self.href = href  


class CoverageTracker:

    def __init__(self, 
                 source: DirectoryPath | FileName | None,
                 runtime_covered_lines: Optional[CoverageStore] = None, 
                 metadata_save_path: Optional[DirectoryPath | FileName | None] = None) -> None:
        self.files: dict[str, FileCoverage] = {}
        self._source = source

        self._store = runtime_covered_lines if runtime_covered_lines is not None else {}
        self._coverage_fails: CoverageStore = {}


        self._metadata_save_path = metadata_save_path

    @cached_property
    def created_at(self) -> str:
        return datetime.now().strftime('%A, %d %B %Y, %H:%M:%S')
    
    @cached_property
    def total(self) -> int:
        return sum(file_coverage.total_statements for file_coverage in self.files.values())

    @cached_property
    def covered(self) -> int:
        return sum(file_coverage.covered_statements for file_coverage in self.files.values())

    @cached_property
    def incorrectly_covered(self) -> int:
        return sum(file_coverage._X_incorrectly_covered_statements for file_coverage in self.files.values())

    @cached_property
    def missing(self) -> int:
        return sum(file_coverage.missing_statements for file_coverage in self.files.values())

    @cached_property
    def correctly_missing(self) -> int:
        return sum(file_coverage._X_correctly_missing_statements for file_coverage in self.files.values())
    
    @cached_property
    def excluded(self) -> int:
        return sum(file_coverage.excluded_statements for file_coverage in self.files.values())

    @cached_property
    def total_score(self) -> float:
        covered = self.covered + self.correctly_missing
        missing = self.missing + self.incorrectly_covered
        return 100.0 * covered / (covered + missing) if covered + missing else 100.0

    @classmethod
    def init_from_store(cls, 
                        source: DirectoryPath | FileName | None, 
                        store: DirectoryPath | FileName | None) -> CoverageTracker:
        return cls(source=source, runtime_covered_lines=CoverageTracker.deserialize(store))

    @classmethod
    def _serialize(cls,
                   _store: CoverageStore,
                   _metadata_save_path: Optional[DirectoryPath | FileName | None] = None,
                   _reconcile: Optional[bool] = False) -> None:
        CoverageTracker(source=None, 
                        runtime_covered_lines=_store, 
                        metadata_save_path=_metadata_save_path).serialize(_reconcile)

    @staticmethod
    def normalize_path(path: str | None) -> Path:
        # If no directory is provided, use the current working directory as the default.
        if path is None:
            path = os.getcwd()

        # If the directory is relative, convert it to an absolute path.
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)

        return Path(path)

    @staticmethod
    def merge(merge_directory: DirectoryPath | FileName | None) -> None:
        # Create a new merged coverage metadata file from all coverage metadata in the target directory.
        merge_path = CoverageTracker.normalize_path(merge_directory)

        coverage_file_names = set()
        _store: CoverageStore = {}
        skips = 0
        merged_count = 0
        for root, _, files in os.walk(merge_path):
            for file in files:
                # Skip files that do not match the coverage metadata file pattern.
                if not file.startswith(METADATA_FILE):
                    continue

                coverage_file_names.add(file)

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                    for _cov_file_path, lines in data.items():
                        if _cov_file_path not in _store:
                            _store[_cov_file_path] = set()
                        _store[_cov_file_path].update(lines)
                        
                    merged_count += 1
                except Exception as e:
                    skips += 1

        # Ensure the new file file does not already exist to avoid accidental overwrites.
        new_coverage_file_name = '%s_merged' % METADATA_FILE
        idx = 0
        while new_coverage_file_name in coverage_file_names:
            new_coverage_file_name = '%s_merged_%d' % (METADATA_FILE, idx)
            idx += 1

        merged_file_path = os.path.join(merge_path, new_coverage_file_name)
        
        # Save the merged coverage metadata to a new file.
        with open(merged_file_path, 'w') as f:
            json.dump({file: list(lines) for file, lines in _store.items()}, f)

        if skips > 0:
            print('[*] Skipped <%d> coverage files due to errors.\n' % skips)

        print('Merged <%d> files starting with `%s`' % (merged_count, METADATA_FILE, ))
        print('Merged coverage metadata saved to `%s`\n' % (merged_file_path, ))

    @staticmethod
    def deserialize(store: DirectoryPath | FileName | None) -> CoverageStore:
        '''
        Deserialize the coverage metadata from the specified store path.

        If no store path is provided, the current directory is 
        searched for a coverage metadata file.

        Raises an exception if multiple coverage metadata files are 
        found or if the file content is invalid.

        Returns a CoverageStore containing the coverage data.
        '''
        if not store:
            store_path = Path.cwd()

            coverage_files = list(store_path.glob('%s*' % METADATA_FILE))
            coverage_files = [f for f in coverage_files if f.is_file()]
            
            if len(coverage_files) != 1:
                raise CoverageDeserializationError(len(coverage_files))
            
            store_path = coverage_files[0]

        else:
            store_path = CoverageTracker.normalize_path(store)

        # Validate the requested file name follows the convention.
        if not store_path.name.startswith(METADATA_FILE):
            raise CoverageDeserializationFileNameError(store_path)
        
        coverage_store = {}
        try:
            with open(store_path, 'r') as f:
                data = json.load(f)
                coverage_store = {file: set(lines) for file, lines in data.items()}
        except Exception as e:
            raise CoverageDeserializationFileContentError(store_path) from e
        
        return coverage_store
    
    @staticmethod
    def tracer(storage: CoverageStore, frame: FrameType, *args, **kwargs):
        code = frame.f_code
        file = code.co_filename
        
        file_no = frame.f_lineno

        if file not in storage:
            storage[file] = set()
        storage[file].add(file_no)
        
        return partial(CoverageTracker.tracer, storage)

    @staticmethod
    def get_serialized_path(metadata_save_path: DirectoryPath | FileName | None) -> Path:
        # TODO please do this in the start ... ?

        save_path = CoverageTracker.normalize_path(metadata_save_path)
        
        # Check if the path is a file
        if save_path.is_file() or save_path.name.startswith(METADATA_FILE):
            # Validate the path follows the convention.
            # It should start with <.coverage...>
            if not save_path.name.startswith(METADATA_FILE):
                raise CoverageDeserializationFileNameError(save_path)
                
            # If it exists, we will overwrite it.
            if save_path.exists(follow_symlinks=False):
                ...
            else:
                # If it doesn't exist, we will create it.
                os.makedirs(save_path.parent, exist_ok=True)
        else:
            # The provided path is a path.
            # There are 2 cases for the provided path:
            # 1. The last part of the path follows the convention (starts with METADATA_FILE)
            #       > We save to the requested file after we create the necessary directories
            # 2. The last part of the path does not follow the convention
            #       > We create the necessary directories and the metadata file inside it.

            if not os.path.basename(save_path).startswith(METADATA_FILE):
                save_path = Path(os.path.join(save_path, METADATA_FILE))
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            else:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

        return save_path

    def update_store(self, ext_store: CoverageStore) -> None:
        for file, lines in ext_store.items():
            self._store.setdefault(file, set()).update(lines)

    def update_fails(self, ext_store: CoverageStore) -> None:
        for file, lines in ext_store.items():
            self._coverage_fails.setdefault(file, set()).update(lines)

    def update_covered_store(self) -> None:
        if _V2_COVERAGE:
            # Skip updating the covered store for V2 coverage
            # Only valid if all tests are passing
            # The exception tests are asserted in their 
            # separate test cases as a result this is correct and 
            # intended behavior
            return 
        new_store = {}
        for file, lines in self._store.items():
            new_store[file] = set(lines) - self._coverage_fails.get(file, set())
        self._store = new_store

    def reconcile(self) -> None:
        # TODO maybe change the exception traces to indicate the reconciliation context
        save_path = CoverageTracker.get_serialized_path(self._metadata_save_path)

        from tini_test.integrations.server import _RECONCILATIONS
        reconciliation = next(_RECONCILATIONS)
        
        prefix, suffix = os.path.split(save_path)
        reconcile_path = os.path.join(prefix, '%s_%s' % (suffix, reconciliation))

        stored_coverage = CoverageTracker.deserialize(reconcile_path)

        # Delete the reconciliation file
        os.remove(reconcile_path)

        # Merge the stored coverage data with the current store
        self.update_store(stored_coverage)

    def serialize(self, reconcile: bool = False) -> None:
        '''
        Only in the case where sitecustomize is used, to further track 
        initialization, there may be case where the file exists or not and may be overwritten.
        In case of internal tests this is avoided by using a different metadata save path.
        In any case we must mark the <2> paths in a way we can understand they refer to 
        the same object.
        '''
        # TODO this needs a proper encoding, for now the chances are slim a collision is found.
        save_path = CoverageTracker.get_serialized_path(self._metadata_save_path)
        if reconcile:
            reconciliation = os.getenv('TINI_TEST_RECONCILE_PATH')
            prefix, suffix = os.path.split(save_path)
            reconciliation_path = Path(os.path.join(prefix, '%s_%s' % (suffix, reconciliation)))
            save_path = reconciliation_path

        with open(save_path, 'w') as f:
            json.dump({file: list(lines) for file, lines in self._store.items()}, f)

        print('Saved coverage metadata to:', save_path)
    
    def collect_files_from_source(self) -> None:
        search_path = CoverageTracker.normalize_path(self._source)

        # If source is a file we must only collect a single file
        if search_path.is_file():
            # Also validate the file exists and is a Python file
            if not search_path.exists(follow_symlinks=False) or not search_path.suffix == '.py':
                raise CoverageRequestedForInvalidFile(search_path)

            store = self._store.get(str(search_path), set())
            add_top_levels = search_path in self._store
            file_coverage = FileCoverage(search_path, store, add_top_levels)
            file_coverage.parse_file()

            self.files[str(search_path)] = file_coverage
            return

        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)

                    store = self._store.get(file_path, set())
                    add_top_levels = file_path in self._store
                    file_coverage = FileCoverage(Path(file_path), store, add_top_levels)
                    file_coverage.parse_file()

                    self.files[file_path] = file_coverage

    @staticmethod
    def pad(s: str | int | float, width: int) -> str:
        if isinstance(s, int):
            return '%-*d' % (width, s)
        
        if isinstance(s, float):
            return '%-*s' % (width, '%.1f' % s)
        
        return '%-*s' % (width, str(s))

    @staticmethod
    def _terminal_score_color(score: float) -> str:
        # Black background with colored score text
        match ScoreClass.get_score_category(score):

            case ScoreClass.EXCELLENT:
                color = Color.DARK_GREEN.value

            case ScoreClass.AVERAGE:
                color = Color.DARK_ORANGE.value

            case ScoreClass.POOR:
                color = Color.DARK_RED.value

        return '\033[48;2;0;0;0m%s%*.1f%% \033[0m' % (color, 7, score)

    def show_short_summary(self, long: Optional[bool] = False) -> None:
        self.update_covered_store()
        self.collect_files_from_source()

        self.files = dict(sorted(self.files.items()))
        
        titles = ('Total', 'Run', 'Correctly Missing', 'Missing', 'Incorrectly Run', 'Excluded', 'Score')

        max_titles = max(len(title) for title in titles)
        max_digits = max(len(str(self.total)), 
                         len(str(self.covered)),
                         len(str(self.correctly_missing)),
                         len(str(self.missing)),
                         len(str(self.incorrectly_covered)), 
                         len(str(self.excluded)), 
                         len('100.0'))
        _max = max(max_titles, max_digits)
        

        print(
            'Coverage Summary\n'  \
            '----------------\n'  \
            '%s\n'                \
            '\n'                  \
            '%s\n'                \
                % 
                (
                    '\t'.join(map(self.pad, titles, [_max]*len(titles))),
                    '\t'.join([
                        self.pad(self.total, _max), 
                        self.pad(self.covered, _max), 
                        self.pad(self.correctly_missing, _max), 
                        self.pad(self.missing, _max), 
                        self.pad(self.incorrectly_covered, _max), 
                        self.pad(self.excluded, _max), 
                        self.pad(self._terminal_score_color(self.total_score), _max)
                    ])
                )
        )

        # Do we want to show this on the normal run as well?
        # Also in modes...
        # For now skip it.
        if not long:
            return
        
        _titles = ('File', 'Statements', 'Run', 'Correctly Missing', 'Missing', 'Incorrectly Run', 'Excluded', 'Score')

        max_titles = max(len(title) for title in _titles)
        max_digits = 0

        for file_path, coverage in self.files.items():
            max_digits = max(max_digits, len(str(coverage.total_statements)))
            max_digits = max(max_digits, len(str(coverage.covered_statements)))
            max_digits = max(max_digits, len(str(coverage._X_correctly_missing_statements)))
            max_digits = max(max_digits, len(str(coverage.missing_statements)))
            max_digits = max(max_digits, len(str(coverage._X_incorrectly_covered_statements)))
            max_digits = max(max_digits, len(str(coverage.excluded_statements)))
            max_digits = max(max_digits, len(str(coverage.score)))

        _max = max(max_titles, max_digits)

        print('\t'.join(map(self.pad, _titles, [_max]*len(_titles))))
        print()

        for file_path, coverage in self.files.items():
            print()
            print(file_path)
            print(
                '\t'.join([
                    self.pad('', _max), 
                    self.pad(coverage.total_statements, _max), 
                    self.pad(coverage.covered_statements, _max), 
                    self.pad(coverage._X_correctly_missing_statements, _max), 
                    self.pad(coverage.missing_statements, _max), 
                    self.pad(coverage._X_incorrectly_covered_statements, _max), 
                    self.pad(coverage.excluded_statements, _max), 
                    self.pad(self._terminal_score_color(coverage.score), _max)
                ])
            )
        
    def to_html(self) -> None:
        return HTMLReport.to_html(self)


####################################
############ HTML representations
####################################

class HTMLLine:

    @staticmethod
    def get_html_node(line: Line) -> HTMLNode:
        main_node = HTMLNode(HTMLNodeType.DIV)
        classes = 'code-line %s' % line.status
        if line.is_continuation:
            classes += ' continuation'
        main_node.add_class({'class': classes})

        child_one = HTMLNode(HTMLNodeType.SPAN)
        child_one.add_class({'class': 'line-number'})
        child_one.set_content('%d.' % line.line_number)


        child_two = HTMLNode(HTMLNodeType.SPAN)
        child_three = None


        match line.status:
            case LineStatus.COMMENT:
                child_two.add_class({'class': 'line-content code-comment'})
                child_two.set_content(html.escape(line.line_content))

            case LineStatus.DOCSTRING:
                match line.is_inline_commented:

                    case True:
                        _code, comment = line.get_split_line()

                        child_two.add_class({'class': 'code-docstring'})
                        child_two.set_content(html.escape(_code))
                        
                        child_three = HTMLNode(HTMLNodeType.SPAN)
                        child_three.add_class({'class': 'inline-comment'})
                        child_three.set_content(html.escape(comment))

                    case False:
                        child_two.add_class({'class': 'line-content code-docstring'})
                        child_two.set_content(html.escape(line.line_content))

            case _:
                match line.is_inline_commented:

                    case True:
                        _code, comment = line.get_split_line()

                       
                        child_two.set_content(html.escape(_code))
  
                        child_three = HTMLNode(HTMLNodeType.SPAN)
                        child_three.add_class({'class': 'inline-comment'})                        
                        child_three.set_content(html.escape(comment))

                    case False:
                        child_two.add_class({'class': 'line-content'})
                        child_two.set_content(html.escape(line.line_content))

        
        main_node.add_children(child_one)

        if child_three:
            code_line = HTMLNode(HTMLNodeType.SPAN)
            code_line.add_class({'class': 'line-content'})

            code_line.add_children(child_two)
            code_line.add_children(child_three)
            main_node.add_children(code_line)

        else:
            main_node.add_children(child_two)

        return main_node


class HTMLFileCoverage:

    @staticmethod
    def get_header_node(coverage: FileCoverage, created_at: str) -> HTMLNode:
        header = HTMLNode(HTMLNodeType.DIV)
        header.add_class({'class': 'cov-header'})

        title = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-title'}, 
                'Coverage report for ',

            children=HTMLNode(HTMLNodeType.SPAN, {'class': 'cov-highlight-path'}, 
                                str(coverage.file_path))
        )

        total = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-total'}, 
                'Total statements: ',
            
            children=HTMLNode(HTMLNodeType.SPAN, {'class': 'cov-highlight-total'}, 
                                str(coverage.total_statements))
        )
        
        score = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-score'},
                'Coverage Score: ',

            children=HTMLNode(HTMLNodeType.SPAN, {'class': HTMLReport._css_score_class(coverage.score)}, 
                                '%.1f%%' % coverage.score)
        )

        created = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-created'}, 
                'Created at %s' % created_at
        )

        header.add_children(title)
        header.add_children(total)
        header.add_children(score)
        header.add_children(created)
        return header

    @staticmethod
    def _toolbar_button(status: LineStatus, count: int) -> HTMLNode:
        button = HTMLNode(HTMLNodeType.BUTTON)
        button.add_class({'class': 'cov-toggle %s' % status.value, 'data-status': status.value})
        button.set_content('%d %s' % (count, status.value.replace('-', ' ')))
        return button

    @staticmethod
    def get_toolbar_node(coverage: FileCoverage) -> HTMLNode:
        toolbar = HTMLNode(HTMLNodeType.DIV, {'class': 'cov-toolbar'})

        covered = HTMLFileCoverage._toolbar_button(LineStatus.RUN, 
                                                   coverage.covered_statements)

        correctly_missing = HTMLFileCoverage._toolbar_button(LineStatus.CORRECTLY_MISSING, 
                                                             coverage._X_correctly_missing_statements) 
        
        missing = HTMLFileCoverage._toolbar_button(LineStatus.MISSING, 
                                                   coverage.missing_statements)

        incorrectly_covered = HTMLFileCoverage._toolbar_button(LineStatus.INCORRECTLY_RUN, 
                                                               coverage._X_incorrectly_covered_statements)

        excluded = HTMLFileCoverage._toolbar_button(LineStatus.EXCLUDED, 
                                                    coverage.excluded_statements)

        comment = HTMLFileCoverage._toolbar_button(LineStatus.COMMENT, 
                                                   coverage.comment_lines)
        
        docstring = HTMLFileCoverage._toolbar_button(LineStatus.DOCSTRING, 
                                                     coverage.docstring_lines)
        
        empty = HTMLFileCoverage._toolbar_button(LineStatus.EMPTY, 
                                                 coverage.empty_lines)
        
        toolbar.add_children(covered)
        toolbar.add_children(correctly_missing)
        toolbar.add_children(missing)
        toolbar.add_children(incorrectly_covered)
        toolbar.add_children(excluded)
        toolbar.add_children(comment)
        toolbar.add_children(docstring)
        toolbar.add_children(empty)
        
        return toolbar

    @staticmethod
    def get_html_node(coverage: FileCoverage) -> HTMLNode:
        code_block = HTMLNode(HTMLNodeType.ARTICLE, {'class': 'code-block'})

        code_content = HTMLNode(HTMLNodeType.DIV, {'class': 'code-content'})

        for line in coverage.lines.values():
            code_content.add_children(HTMLLine.get_html_node(line))

        code_block.add_children(code_content)

        return code_block


class HTMLReport:

    @staticmethod
    def init_store() -> Path:
        dest_dir = Path(os.path.join(os.getcwd(), STORE))

        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        os.makedirs(dest_dir, exist_ok=True)
    
        return dest_dir

    @staticmethod
    def add_git_ignore(dest_dir: Path) -> None:
        # Also generate a .gitignore file to ignore all generated HTML files.
        with open(os.path.join(dest_dir, '.gitignore'), 'w', encoding='utf-8') as f:
            f.write('*')

    @staticmethod
    def add_style(dest_dir: Path) -> None:
        with open(os.path.join(os.path.dirname(__file__), STYLE_FILE), 'r') as f:
            content = f.read()
        
        with open(os.path.join(dest_dir, STYLE_FILE), 'w') as f:
            f.write(content)

    @staticmethod
    def coverage_script() -> HTMLNode:
        script = HTMLNode(HTMLNodeType.SCRIPT)
        script.set_content(_TOGGLE_SCRIPT)
        return script
    
    @staticmethod
    def add_svg(dest_dir: Path, score: float) -> None:
        color = HTMLReport._svg_score_gradient(score)
        with open(os.path.join(os.path.dirname(__file__), SVG_FILE), 'r') as f:
            svg = f.read()

        svg = svg.replace('url(#greenGradient)', 'url(#%s)' % color)

        _score = '%0.1f' % score

        if _score.endswith('.0'):
            svg = svg.replace('-1%', '%s%%' % _score.replace('.0', ''))
        else:
            svg = svg.replace('-1%', '%0.1f%%' % score)

        with open(os.path.join(dest_dir, SVG_FILE), 'w') as f:
            f.write(svg)

    @staticmethod
    def _css_score_class(score: float) -> str:
        match ScoreClass.get_score_category(score):

            case ScoreClass.EXCELLENT:
                return 'score-good'
            
            case ScoreClass.AVERAGE:
                return 'score-ok'
            
            case ScoreClass.POOR:
                return 'score-bad'

    @staticmethod
    def _svg_score_gradient(score: float) -> str:
        match ScoreClass.get_score_category(score):

            case ScoreClass.EXCELLENT:
                return 'greenGradient'
            
            case ScoreClass.AVERAGE:
                return 'orangeGradient'
            
            case ScoreClass.POOR:
                return 'redGradient'
            
    @staticmethod
    def get_hyper_links_and_update_coverage_hrefs(tracker: CoverageTracker) -> list[HTMLHyperLink]:
        links = []

        for idx, (file_path, coverage) in enumerate(tracker.files.items()):
            href = ('%d_%s.html' 
                        % 
                        (
                            idx, 
                            Path(file_path).stem, 
                        )
                    )
            coverage.set_href(href)

            links.append(HTMLHyperLink(href=href, text=file_path))

        return links
    
    @staticmethod
    def get_index_content(tracker: CoverageTracker) -> HTMLNode:
        hyper_links = HTMLReport.get_hyper_links_and_update_coverage_hrefs(tracker)

        header = HTMLNode(HTMLNodeType.DIV, {'class': 'cov-header'})
        header.add_children([

            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-title'}, 
                     'Coverage report'),

            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-total'}, 
                     '%d files' % len(tracker.files)),

            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-score %s' % HTMLReport._css_score_class(tracker.total_score)},
                     'Total coverage %.1f%%' % tracker.total_score),

            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-created'}, 
                     'Created at %s' % tracker.created_at)
        ])

        table = HTMLNode(HTMLNodeType.TABLE)
        table.add_class({'class': 'index-table'})

        head_row = HTMLNode(HTMLNodeType.TR)

        for title in ('File', 'Statements', 'Run', 'Correctly Missing', 'Missing', 'Incorrectly Run','Excluded', 'Score'):
            title_node = HTMLNode(HTMLNodeType.TH,
                                  {'class': 'index-file' if title == 'File' else 'index-num'},
                                  title)
            head_row.add_children(title_node)

        table.add_children(head_row)
        
        for link, coverage in zip(hyper_links, tracker.files.values()):
            row = HTMLNode(HTMLNodeType.TR)
            row.add_children([
                HTMLNode(HTMLNodeType.TD, {'class': 'index-file'}, link.to_html()),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.total_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.covered_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage._X_correctly_missing_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.missing_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage._X_incorrectly_covered_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.excluded_statements)),
            ])
            _score = HTMLNode(HTMLNodeType.TD)
            _score.add_class({'class': 'index-num %s' % HTMLReport._css_score_class(coverage.score)})
            _score.content = '%.1f%%' % coverage.score

            row.add_children(_score)
            table.add_children(row)

        total_row = HTMLNode(HTMLNodeType.TR)
        total_row.add_children([
            HTMLNode(HTMLNodeType.TD, {'class': 'index-file'}, 'Total'),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.total)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.covered)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.correctly_missing)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.missing)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.incorrectly_covered)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.excluded)),
        ])
        _total_score = HTMLNode(HTMLNodeType.TD)
        _total_score.add_class({'class': 'index-num %s' % HTMLReport._css_score_class(tracker.total_score)})
        _total_score.content = '%.1f%%' % tracker.total_score

        total_row.add_children(_total_score)
        table.add_children(total_row)

        page = HTMLNode(HTMLNodeType.DIV)
        page.add_children(header)
        page.add_children(table)
        
        return page

    @staticmethod
    def to_html(tracker: CoverageTracker) -> None:
        tracker.update_covered_store()
        tracker.collect_files_from_source()

        tracker.files = dict(sorted(tracker.files.items()))

        dest_dir = HTMLReport.init_store()
        HTMLReport.add_git_ignore(dest_dir)
        HTMLReport.add_style(dest_dir)
    
        index = HTMLTemplate(file_path=Path(os.path.join(dest_dir, 'index.html')), 
                             content=HTMLReport.get_index_content(tracker).to_html())
        index.write_to_file()

        for coverage in tracker.files.values():

            coverage_path = Path(os.path.join(dest_dir, coverage.href))

            page = HTMLNode(HTMLNodeType.DIV)
            page.add_children(HTMLFileCoverage.get_header_node(coverage, tracker.created_at))
            page.add_children(HTMLFileCoverage.get_toolbar_node(coverage))
            page.add_children(HTMLFileCoverage.get_html_node(coverage))
            page.add_children(HTMLReport.coverage_script())

            tmpl = HTMLTemplate(file_path=coverage_path, content=page.to_html())
            tmpl.write_to_file()

        HTMLReport.add_svg(dest_dir, tracker.total_score)

        print('Coverage report generated at %s\n' % dest_dir)
        tracker.show_short_summary(long=True)
