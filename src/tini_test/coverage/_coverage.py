from __future__ import annotations
import html
import io
import json
import os
import shutil
from collections import Counter
from datetime import datetime
from functools import cached_property, partial
from pathlib import Path
import tokenize
from types import FrameType
from typing import Optional

from tini_test._internals._ast_utils import AstParser
from tini_test.coverage.consts import (_TOGGLE_SCRIPT, METADATA_FILE, STORE,
                                       STYLE_FILE, SVG_FILE)
from tini_test.coverage.enums import HTMLNodeType, LineStatus
from tini_test.coverage.html import HTMLHyperLink, HTMLNode, HTMLTemplate
from tini_test.enums import Color, ScoreClass
from tini_test.misc.annotations import (CodeLineNumber, CoverageStore,
                                        DirectoryPath, FileName, LineContent,
                                        StatementId)
from tini_test.misc.exceptions import (CoverageDeserializationError,
                                       CoverageDeserializationFileContentError,
                                       CoverageDeserializationFileNameError,
                                       CoverageRequestedForInvalidFile)

# TODO
# Add someting for exclude?
# Fall back behavior for to_html of report?
# Top levels are gathered manually @core?


class InlineComment:

    def __init__(self, _start: int) -> None:
        self.start = _start

    @classmethod
    def from_source(cls, source: str) -> dict[CodeLineNumber, InlineComment]:
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

    @property
    def is_inline_commented(self) -> bool:
        return self.inline_comment is not None

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
    def __init__(self, file_path: Path, runtime_covered_lines: set[CodeLineNumber]) -> None:
        self.href = ''

        self.file_path = file_path
        self.lines: dict[CodeLineNumber, Line] = {}

        with open(self.file_path, 'r') as f:
            source = f.read()

        self.inline_comments = InlineComment.from_source(source)

        self._statement_status: dict[StatementId, LineStatus] = {}
        self._statement_counts: Counter[LineStatus] = Counter()

        self.parser = AstParser.from_file_read(source, str(self.file_path))
        self.update_covered_statements(runtime_covered_lines)

        self.update_state(source.splitlines())

    @staticmethod
    def is_docstring_se(line: str) -> bool:
        return line.startswith('"""') or line.startswith("'''") or line.endswith('"""') or line.endswith("'''")
    
    @cached_property
    def line_to_statement(self) -> dict[CodeLineNumber, StatementId]:
        return self.parser.extract_line_to_statement()

    @cached_property
    def statement_to_lines(self) -> dict[StatementId, list[CodeLineNumber]]:
        _statement_to_lines: dict[StatementId, list[CodeLineNumber]] = {}

        for line_number, statement in self.line_to_statement.items():
            _statement_to_lines.setdefault(statement, []).append(line_number)

        return _statement_to_lines
    
    @property
    def top_levels(self) -> list[CodeLineNumber]:
        return self.parser.extract_top_level_lines()
    
    @property
    def total_statements(self) -> int:
        return len(self.statement_to_lines)

    @property
    def covered_statements(self) -> int:
        return self._statement_counts[LineStatus.RUN]

    @property
    def missing_statements(self) -> int:
        return self._statement_counts[LineStatus.MISSING]
    
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
        total = run + missing
        return 100.0 * run / total if total else 100.0

    def update_covered_statements(self, runtime_covered_lines: set[CodeLineNumber]) -> None:
        run_statements = set()

        runtime_covered_lines.discard(0)
        
        # Update covered statements based on runtime covered.
        for line in runtime_covered_lines:
            if line in self.line_to_statement:
                run_statements.add(self.line_to_statement[line])

        # Include top-level statements as covered.
        for line in self.top_levels:
            if line in self.line_to_statement:
                run_statements.add(self.line_to_statement[line])

        for statement in self.statement_to_lines:

            status = LineStatus.MISSING

            if statement in run_statements:
                status = LineStatus.RUN

            self._statement_status[statement] = status
            self._statement_counts[status] += 1
    
    def update_state(self, data: list[str]) -> None:
        have_docstring_open = False

        for l_no, l_cont in enumerate(data, start=1):
            owner = self.line_to_statement.get(l_no)
            stripped = l_cont.strip()

            inline_comment = self.inline_comments.get(l_no)

            if owner is None or not stripped or stripped.startswith('#'):

                # Line is empty
                if not stripped:
                    if have_docstring_open:
                        self.lines[l_no] = Line(l_no, l_cont, LineStatus.DOCSTRING)
                    else:
                        self.lines[l_no] = Line(l_no, l_cont, LineStatus.EMPTY)
                        self._statement_counts[LineStatus.EMPTY] += 1

                # Line is comment
                elif stripped.startswith('#'):
                    if have_docstring_open:
                        self.lines[l_no] = Line(l_no, l_cont, LineStatus.DOCSTRING)
                    else:
                        self.lines[l_no] = Line(l_no, l_cont, LineStatus.COMMENT)
                        self._statement_counts[LineStatus.COMMENT] += 1

                # Line must be part of a docstring
                else:
                    # Else/finally blocks are skipped @extract_line_to_statement
                    if stripped.startswith('else:') or stripped.startswith('finally:'):
                        # @Comments are allowed here
                        if inline_comment:
                            self._statement_counts[LineStatus.COMMENT] += 1
                        self.lines[l_no] = Line(l_no, l_cont, LineStatus.EXCLUDED, inline_comment=inline_comment)
                        self._statement_counts[LineStatus.EXCLUDED] += 1
                    else:
                        self.lines[l_no] = Line(l_no, l_cont, LineStatus.DOCSTRING)
                        
                        # We are inside a valid syntaxed Python file.
                        if self.is_docstring_se(stripped):

                            match have_docstring_open:

                                case False:
                                    self._statement_counts[LineStatus.DOCSTRING] += 1
                                    have_docstring_open = True

                                case True:
                                    # @Comments are allowed at the end of the docstring
                                    if inline_comment:
                                        self.lines[l_no].add_inline_comment(inline_comment)
                                        self._statement_counts[LineStatus.COMMENT] += 1
                                    have_docstring_open = False
                                    
            else:
                is_continuation = l_no != self.statement_to_lines[owner][0]
                status = self._statement_status[owner]
                self.lines[l_no] = Line(l_no, l_cont, status, is_continuation, inline_comment)
                if inline_comment:
                    self._statement_counts[LineStatus.COMMENT] += 1

    def set_href(self, href: str) -> None:
        self.href = href      
      

class CoverageTracker:

    def __init__(self, 
                 source: DirectoryPath | FileName | None,
                 runtime_covered_lines: CoverageStore, 
                 metadata_save_path: Optional[DirectoryPath | FileName | None] = None) -> None:
        self.files: dict[str, FileCoverage] = {}
        self._source = source
        self._store = runtime_covered_lines
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
    def missing(self) -> int:
        return sum(file_coverage.missing_statements for file_coverage in self.files.values())

    @cached_property
    def excluded(self) -> int:
        return sum(file_coverage.excluded_statements for file_coverage in self.files.values())

    @cached_property
    def total_score(self) -> float:
        covered = self.covered
        missing = self.missing
        return 100.0 * covered / (covered + missing) if covered + missing else 100.0


    @classmethod
    def init_from_store(cls, 
                        source: DirectoryPath | FileName | None, 
                        store: DirectoryPath | FileName | None) -> CoverageTracker:
        return cls(source=source, runtime_covered_lines=CoverageTracker.deserialize(store))
    
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

        # Very slow
        # filename = os.path.abspath(frame.f_code.co_filename)

        # _return  = partial(CoverageTracker.tracer, storage)

        # if not filename.endswith('.py'):
        #     return _return
        
        # if not filename.startswith(apply_at):
        #     return _return

        # if 'site-packages' in filename:
        #     return _return

        # if 'tINI-test/src' in filename:
        #     return _return
        
        file_no = frame.f_lineno

        if file not in storage:
            storage[file] = set()
        storage[file].add(file_no)
        
        return partial(CoverageTracker.tracer, storage)

    def serialize(self) -> None:
        save_path = CoverageTracker.normalize_path(self._metadata_save_path)

        # Check if the path is a file
        if save_path.is_file():
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
            # If the path is not a file, we will create the necessary directories.
            os.makedirs(save_path, exist_ok=True)
            save_path = Path(os.path.join(save_path, METADATA_FILE))

        with open(save_path, 'w') as f:
            json.dump({file: list(lines) for file, lines in self._store.items()}, f)

    def collect_files_from_source(self) -> None:
        search_path = CoverageTracker.normalize_path(self._source)

        # If source is a file we must only collect a single file
        if search_path.is_file():
            # Also validate the file exists and is a Python file
            if not search_path.exists(follow_symlinks=False) or not search_path.suffix == '.py':
                raise CoverageRequestedForInvalidFile(search_path)

            
            store = self._store.get(str(search_path), set())
            self.files[str(search_path)] = FileCoverage(search_path, store)
            return

        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    store = self._store.get(file_path, set())
                    self.files[file_path] = FileCoverage(Path(file_path), store)

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

        self.collect_files_from_source()
        self.files = dict(sorted(self.files.items()))
        
        titles = ('Total', 'Covered', 'Missing', 'Excluded', 'Score')

        max_titles = max(len(title) for title in titles)
        max_digits = max(len(str(self.total)), 
                         len(str(self.covered)), 
                         len(str(self.missing)), 
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
                        self.pad(self.missing, _max), 
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
        
        _titles = ('File', 'Statements', 'Run', 'Missing', 'Excluded', 'Score')

        max_titles = max(len(title) for title in _titles)
        max_digits = 0

        for file_path, coverage in self.files.items():
            max_digits = max(max_digits, len(str(coverage.total_statements)))
            max_digits = max(max_digits, len(str(coverage.covered_statements)))
            max_digits = max(max_digits, len(str(coverage.missing_statements)))
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
                    self.pad(coverage.missing_statements, _max), 
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
        button.add_class({'class': 'cov-toggle %s' % status, 'data-status': str(status)})
        button.set_content('%d %s' % (count, status))
        return button

    @staticmethod
    def get_toolbar_node(coverage: FileCoverage) -> HTMLNode:
        toolbar = HTMLNode(HTMLNodeType.DIV, {'class': 'cov-toolbar'})

        covered = HTMLFileCoverage._toolbar_button(LineStatus.RUN, 
                                                   coverage.covered_statements)
        
        missing = HTMLFileCoverage._toolbar_button(LineStatus.MISSING, 
                                                   coverage.missing_statements)

        excluded = HTMLFileCoverage._toolbar_button(LineStatus.EXCLUDED, 
                                                    coverage.excluded_statements)

        comment = HTMLFileCoverage._toolbar_button(LineStatus.COMMENT, 
                                                   coverage.comment_lines)
        
        docstring = HTMLFileCoverage._toolbar_button(LineStatus.DOCSTRING, 
                                                     coverage.docstring_lines)
        
        empty = HTMLFileCoverage._toolbar_button(LineStatus.EMPTY, 
                                                 coverage.empty_lines)
        
        toolbar.add_children(covered)
        toolbar.add_children(missing)
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

        for title in ('File', 'Statements', 'Run', 'Missing', 'Excluded', 'Score'):
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
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.missing_statements)),
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
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(tracker.missing)),
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
