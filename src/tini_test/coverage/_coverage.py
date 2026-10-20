import json
import os
import shutil
from collections import Counter
from datetime import datetime
from functools import cached_property, partial
from pathlib import Path
from typing import Optional

from tini_test._internals._ast_utils import AstParser
from tini_test.coverage.consts import (_TOGGLE_SCRIPT, METADATA_FILE, STORE,
                                       STYLE_FILE)
from tini_test.coverage.enums import HTMLNodeType, LineCoverageStatus
from tini_test.coverage.html import HTMLHyperLink, HTMLNode, HTMLTemplate
from tini_test.misc.annotations import (CodeLineNumber, CoverageStore,
                                        DirectoryPath, FileName, LineContent, StatementId)

# XXX test coverage integration

class LineStats:
    def __init__(self, 
                 line_number: CodeLineNumber, 
                 line_content: LineContent, 
                 status: LineCoverageStatus,
                 is_continuation: bool = False) -> None:
        self.line_number = line_number
        self.line_content = line_content
        self.status = status
        # Not the first line of a multi line statement.
        self.is_continuation = is_continuation

    def get_html_node(self) -> HTMLNode:
        main_node = HTMLNode(HTMLNodeType.DIV)
        classes = 'code-line %s' % self.status
        if self.is_continuation:
            classes += ' continuation'
        main_node.add_class({'class': classes})

        child_one = HTMLNode(HTMLNodeType.SPAN)
        child_one.add_class({'class': 'line-number'})
        child_one.set_content('%d.' % self.line_number)

        child_two = HTMLNode(HTMLNodeType.SPAN)
        child_two.add_class({'class': 'line-content'})
        child_two.set_content(self.line_content)

        main_node.add_children(child_one)
        main_node.add_children(child_two)

        return main_node


class FileCoverage:
    # Maybe split it into functions class for better modularity
    def __init__(self, file_path: Path, runtime_covered_lines: set[CodeLineNumber]) -> None:
        self.href = ''

        self.file_path = file_path

        with open(self.file_path, 'r') as f:
            source = f.read()

        data = source.splitlines()
        self.parser = AstParser.from_file_read(source, str(self.file_path))

        self.statement_counts: Counter[LineCoverageStatus] = Counter()
        self.statement_status: dict[StatementId, LineCoverageStatus] = {}

        self.lines: dict[CodeLineNumber, LineStats] = self.parse_file(data, runtime_covered_lines)

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
        return self.parser.extract_top_level_import_lines()
    
    @property
    def total_statements(self) -> int:
        return len(self.statement_to_lines)

    @property
    def covered_statements(self) -> int:
        return self.statement_counts[LineCoverageStatus.RUN]

    @property
    def missing_statements(self) -> int:
        return self.statement_counts[LineCoverageStatus.MISSING]
    
    @property
    def excluded_statements(self) -> int:
        return self.statement_counts[LineCoverageStatus.EXCLUDED]
    
    @property
    def empty_lines(self) -> int:
        return self.statement_counts[LineCoverageStatus.EMPTY]

    @property
    def score(self) -> float:
        run, missing = self.covered_statements, self.missing_statements
        total = run + missing
        return 100.0 * run / total if total else 100.0

    def update_covered_statements(self, runtime_covered_lines: set[CodeLineNumber]) -> None:
        run_statements = set()

        # Update covered statements based on runtime covered lines.
        for line in runtime_covered_lines:
            if line in self.line_to_statement:
                run_statements.add(self.line_to_statement[line])

        # Include top-level import statements as covered.
        # This should also include most globals.
        for line in self.top_levels:
            if line in self.line_to_statement:
                run_statements.add(self.line_to_statement[line])

        # TODO add someting for exclude
        for statement in self.statement_to_lines:

            status = LineCoverageStatus.MISSING

            if statement in run_statements:
                status = LineCoverageStatus.RUN

            self.statement_status[statement] = status
            self.statement_counts[status] += 1

    def parse_file(self, data: list[str], runtime_covered_lines: set[CodeLineNumber]) -> dict[CodeLineNumber, LineStats]:
        
        self.update_covered_statements(runtime_covered_lines)
        
        lines = {}
        for line_number, line_content in enumerate(data, start=1):
            owner = self.line_to_statement.get(line_number)
            stripped = line_content.strip()

            # Blank and comment lines inside a multi line statement are still empty lines.
            if owner is None or not stripped or stripped.startswith('#'):
                lines[line_number] = LineStats(line_number, line_content, LineCoverageStatus.EMPTY)
                self.statement_counts[LineCoverageStatus.EMPTY] += 1
                continue

            lines[line_number] = LineStats(
                line_number,
                line_content,
                self.statement_status[owner],
                is_continuation=line_number != self.statement_to_lines[owner][0],
            )
        
        return lines

    def set_href(self, href: str) -> None:
        self.href = href      

    def get_header_node(self, created_at: str) -> HTMLNode:
        header = HTMLNode(HTMLNodeType.DIV)
        header.add_class({'class': 'cov-header'})

        title = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-title'}, 'Coverage report for ',
            HTMLNode(HTMLNodeType.SPAN, {'class': 'cov-highlight-path'}, str(self.file_path))
        )

        total = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-total'}, 'Total statements: ',
            HTMLNode(HTMLNodeType.SPAN, {'class': 'cov-highlight-total'}, str(self.total_statements))
        )
       
        score = HTMLNode(
            HTMLNodeType.DIV, {'class': 'cov-score'}, 'Coverage Score: ',
            HTMLNode(HTMLNodeType.SPAN, {'class': 'cov-highlight-score'}, '%.1f%%' % self.score)
        )

        created = HTMLNode(HTMLNodeType.DIV, {'class': 'cov-created'}, 'Created at %s' % created_at)

        header.add_children(title)
        header.add_children(total)
        header.add_children(score)
        header.add_children(created)
        return header

    @staticmethod
    def _toolbar_button(status: LineCoverageStatus, count: int) -> HTMLNode:
        button = HTMLNode(HTMLNodeType.BUTTON)
        button.add_class({'class': 'cov-toggle %s' % status, 'data-status': str(status)})
        button.set_content('%d %s' % (count, status))
        return button

    def get_toolbar_node(self) -> HTMLNode:
        toolbar = HTMLNode(HTMLNodeType.DIV, {'class': 'cov-toolbar'})

        covered = self._toolbar_button(LineCoverageStatus.RUN, self.covered_statements)
        missing = self._toolbar_button(LineCoverageStatus.MISSING, self.missing_statements)
        empty = self._toolbar_button(LineCoverageStatus.EMPTY, self.empty_lines)
        excluded = self._toolbar_button(LineCoverageStatus.EXCLUDED, self.excluded_statements)

        toolbar.add_children(covered)
        toolbar.add_children(missing)
        toolbar.add_children(empty)
        toolbar.add_children(excluded)

        return toolbar

    def get_html_node(self) -> HTMLNode:
        code_block = HTMLNode(HTMLNodeType.ARTICLE, {'class': 'code-block'})

        code_content = HTMLNode(HTMLNodeType.DIV, {'class': 'code-content'})

        for line in self.lines.values():
            code_content.add_children(line.get_html_node())

        code_block.add_children(code_content)

        return code_block
      

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
    def coverage_script(self) -> HTMLNode:
        script = HTMLNode(HTMLNodeType.SCRIPT)
        script.set_content(_TOGGLE_SCRIPT)
        return script

    @classmethod
    def init_from_store(cls, 
                        source: DirectoryPath | FileName | None, 
                        store: DirectoryPath | FileName | None) -> 'CoverageTracker':
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
            print('Skipped <%d> coverage files due to errors.' % skips)

        print('Merged <%d> coverage metadata saved to `%s`' % (merged_count, merged_file_path))

    @staticmethod
    def deserialize(store: DirectoryPath | FileName | None) -> CoverageStore:
        # If not path is specified. Attempt to search the current directory for the coverage metadata file.
        # If we find more then one coverage metadata file, we should raise an exception to avoid ambiguity.
        if not store:
            store_path = Path.cwd()

            coverage_files = list(store_path.glob('%s*' % METADATA_FILE))
            coverage_files = [f for f in coverage_files if f.is_file()]
            if not coverage_files:
                # TODO add exception
                raise FileNotFoundError('No coverage metadata file found in the current directory.')
            if len(coverage_files) > 1:
                # TODO add exception
                raise ValueError('Multiple coverage metadata files found in the current directory. Please specify one explicitly.')
            store_path = coverage_files[0]

        else:
            store_path = CoverageTracker.normalize_path(store)

        # Validate the requested file name follows the convention.
        if not store_path.name.startswith(METADATA_FILE):
            # TODO add exception
            raise ValueError('The metadata file must start with "%s"' % METADATA_FILE)
        
        coverage_store = {}
        with open(store_path, 'r') as f:
            data = json.load(f)
            coverage_store = {file: set(lines) for file, lines in data.items()}

        return coverage_store
    
    @staticmethod
    def tracer(storage: CoverageStore, frame, *args, **kwargs):
        code = frame.f_code
        file = code.co_filename
        file_no = frame.f_lineno

        # Should we consider using the target in this context?
        if file not in storage:
            storage[file] = set()
        storage[file].add(file_no)
        
        return partial(CoverageTracker.tracer, storage)

    @staticmethod
    def _score_class(score: float) -> str:
        if score >= 80:
            return 'score-good'
        if score >= 50:
            return 'score-ok'
        return 'score-bad'

    def serialize(self) -> None:
        save_path = CoverageTracker.normalize_path(self._metadata_save_path)

        # Check if the path is a file
        if save_path.is_file():
            # Validate the path follows the convention.
            # It should start with <.coverage...>
            if not save_path.name.startswith(METADATA_FILE):
                # TODO add exception
                raise ValueError('The metadata file must start with "%s"' % METADATA_FILE)

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
                print('Rejected: file not found or not a Python file.')
                # TODO add exception here?
                return
            store = self._store.get(str(search_path), set())
            self.files[str(search_path)] = FileCoverage(search_path, store)
            return

        for root, _, files in os.walk(search_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    store = self._store.get(file_path, set())
                    self.files[file_path] = FileCoverage(Path(file_path), store)

    def init_store(self, dest_dir: Path) -> None:
        if dest_dir.exists():
            # input('Will remove <%s>, press Enter to continue...' % dest_dir)
            shutil.rmtree(dest_dir)

        os.makedirs(dest_dir, exist_ok=True)
        self.add_style(dest_dir)

    def add_style(self, dest_dir: Path) -> None:
        with open(os.path.join(os.path.dirname(__file__), STYLE_FILE), 'r') as f:
            content = f.read()
        
        with open(os.path.join(dest_dir, STYLE_FILE), 'w') as f:
            f.write(content)

    def get_hyper_links_and_update_coverage_hrefs(self) -> list[HTMLHyperLink]:
        links = []

        for idx, (file_path, coverage) in enumerate(self.files.items()):
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

    def get_index_content(self) -> HTMLNode:
        hyper_links = self.get_hyper_links_and_update_coverage_hrefs()

        files = list(self.files.values())
        run = sum(c.covered_statements for c in files)
        missing = sum(c.missing_statements for c in files)
        total_score = 100.0 * run / (run + missing) if run + missing else 100.0

        header = HTMLNode(HTMLNodeType.DIV, {'class': 'cov-header'})
        header.add_children([
            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-title'}, 'Coverage report'),
            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-total'}, '%d files' % len(self.files)),
            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-score %s' % self._score_class(total_score)},
                     'Total coverage %.1f%%' % total_score),
            HTMLNode(HTMLNodeType.DIV, {'class': 'cov-created'}, 'Created at %s' % self.created_at)
        ])


        table = HTMLNode(HTMLNodeType.TABLE)
        table.add_class({'class': 'index-table'})

        head_row = HTMLNode(HTMLNodeType.TR)
        for title in ('File', 'Statements', 'Run', 'Missing', 'Excluded', 'Score'):
            head_row.add_children(HTMLNode(HTMLNodeType.TH,
                                           {'class': 'index-file' if title == 'File' else 'index-num'},
                                           title))
        table.add_children(head_row)
        
        for link, coverage in zip(hyper_links, self.files.values()):
            row = HTMLNode(HTMLNodeType.TR)
            row.add_children([
                HTMLNode(HTMLNodeType.TD, {'class': 'index-file'}, link.to_html()),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.total_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.covered_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.missing_statements)),
                HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(coverage.excluded_statements)),
            ])
            _score = HTMLNode(HTMLNodeType.TD)
            _score.add_class({'class': 'index-num %s' % self._score_class(coverage.score)})
            _score.content = '%.1f%%' % coverage.score

            row.add_children(_score)
            table.add_children(row)

        total_row = HTMLNode(HTMLNodeType.TR)
        total_row.add_children([
            HTMLNode(HTMLNodeType.TD, {'class': 'index-file'}, 'Total'),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(sum(c.total_statements for c in files))),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(run)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(missing)),
            HTMLNode(HTMLNodeType.TD, {'class': 'index-num'}, str(sum(c.excluded_statements for c in files))),
        ])
        _total_score = HTMLNode(HTMLNodeType.TD)
        _total_score.add_class({'class': 'index-num %s' % self._score_class(total_score)})
        _total_score.content = '%.1f%%' % total_score

        total_row.add_children(_total_score)
        table.add_children(total_row)

        page = HTMLNode(HTMLNodeType.DIV)
        page.add_children(header)
        page.add_children(table)
        return page

    def to_html(self) -> None:
        self.collect_files_from_source()

        dest_dir = Path(os.path.join(os.getcwd(), STORE))

        self.init_store(dest_dir)
    
        index = HTMLTemplate(file_path=Path(os.path.join(dest_dir, 'index.html')), 
                             content=self.get_index_content().to_html())
        index.write_to_file()

        for coverage in self.files.values():

            coverage_path = Path(os.path.join(dest_dir, coverage.href))

            page = HTMLNode(HTMLNodeType.DIV)
            page.add_children(coverage.get_header_node(self.created_at))
            page.add_children(coverage.get_toolbar_node())
            page.add_children(coverage.get_html_node())
            page.add_children(self.coverage_script)

            tmpl = HTMLTemplate(file_path=coverage_path, content=page.to_html())
            tmpl.write_to_file()
    
        print('Coverage report generated at %s' % os.path.join(os.getcwd(), STORE))