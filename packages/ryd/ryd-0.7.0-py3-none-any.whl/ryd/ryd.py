# coding: utf-8

from __future__ import annotations

import glob
import sys
import argparse
from textwrap import dedent
from ruamel.std.pathlib import Path
from ruamel.yaml import YAML

from typing import Any, Union, Optional, List, Tuple


Bugs = """\
- check empty documents. E.g. !python that only has code in !pre, and !stdout
  without any introductory text
"""

ToDo = """\
- some mechanism to show the name, leave option for 'skipping'/'converting'
  comment and push out newline later. Test incombination with verbosity
- specify Python interpreter, or create virtualenv + package installs, in a better
  way than using RYD_PYTHON env var.
- formalize temporary directory
- store (prefixed) program, only execute when !stdout is requested.
- parse messages like:
  README.rst:72: (ERROR/3) Inconsistent literal block quoting.
  and show output context
- zoom in on errors that have no line number: `some name <>`__
- document handling of :: in RST, and need for |+ in stdraw
- describe yaml comments after `|+ # `
- support code-block directive  http://rst2pdf.ralsina.me/handbook.html#syntax-highlighting
- list structure of the .ryd file
- process documents using xyz:prog  matching the document tag xyz by rt piping through prog
- why do toplevel LiteralScalarString dumps have |2, it is not even correct!
= consider moving to plugin system
"""


class RydExecError(Exception):
    pass


class RYD:
    def __init__(self, args: argparse.Namespace, config: Optional[Any] = None) -> None:
        self._args = args
        self._config = config
        self._name_printed = False
        self._current_path: Union[Path, None] = None

    def convert(self) -> None:
        for file_name in self._args.file:
            self._name_printed = False
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    self.convert_one(Path(exp_file_name), verbose=self._args.verbose)
                continue
            self.convert_one(Path(file_name), verbose=self._args.verbose)

    def clean(self) -> None:
        for file_name in self._todo():
            self.convert_one(file_name, clean=True)

    def _todo(self) -> list[Path]:
        todo = []
        for file_name in self._args.file:
            self._name_printed = False
            if file_name[0] == '*':
                for exp_file_name in sorted(Path('.').glob(file_name)):
                    todo.append(exp_file_name)
                    continue
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    todo.append(Path(exp_file_name))
                continue
            todo.append(Path(file_name))
        # print('todo', todo)
        return todo

    def name(self) -> None:
        """print name of file only once (either verbose or on error)"""
        if self._name_printed:
            return
        self._name_printed = True
        print(self._current_path)

    def convert_one(self, path: Path, clean: bool = False, verbose: int = 0) -> None:
        if self._current_path is None and not path.exists():
            print('unknown command, or file:', path)
            sys.exit(1)
        self._current_path = path
        if verbose > 0:
            self.name()
        yaml = YAML()
        Conv: Any = None
        ys = YamlDocStreamSplitter(path)
        it = ys.iter()
        cx = it.next(yaml)
        if 0.199 < float(cx['version']) < 0.201:
            if 'output' in cx:
                text = cx['output']
                print('should change "output: {text} in metadata to "text: {text}"')
            else:
                text = cx['text']
            if text == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor2 as Conv  # type: ignore # NOQA
            elif text == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor2 as Conv  # type: ignore # NOQA
            elif text == 'md':
                from ryd._convertor.markdown import MarkdownConvertor2 as Conv  # type: ignore # NOQA
        elif 0.099 < float(cx['version']) < 0.101:
            if cx['output'] == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor as Conv  # type: ignore # NOQA
            elif cx['output'] == 'md':
                from ryd._convertor.markdown import MarkdownConvertor as Conv  # type: ignore # NOQA
            elif cx['output'] == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor as Conv  # type: ignore # NOQA
            else:
                raise NotImplementedError
        assert Conv is not None
        convertor = Conv(self, yaml, cx, path)
        if clean:
            convertor.clean()
            return
        if not convertor.check():
            return
        while not it.done():
            y = it.next()
            # print('y', y)
            if y is None:
                break
            try:
                x = yaml.load(y)
            except Exception as e:
                print(f'====== doc =====\n{y.decode("utf-8")}\n=======================')
                print('exception', e)
                raise
            # print('x', repr(x))
            if not convertor(x):  # already up-to-date
                sys.stdout.flush()
                # ToDo you cannot return here, the PDF might not be generated because
                # of some rst2pdf issue
                return
        if convertor.updated:
            if verbose > 0:
                print('updated')
        convertor.write()
        # convertor.dump()
        sys.stdout.flush()

    def from_rst(self) -> None:
        from .loadrst import LoadRST

        for file_name in (Path(f) for f in self._args.file):
            ryd_name = file_name.with_suffix('.ryd')
            if ryd_name.exists() and not self._args.force:
                print('skipping', ryd_name)
                continue
            rst = LoadRST(file_name)
            rst.analyse_sections()
            print('writing', ryd_name)
            with ryd_name.open('w') as fp:
                fp.write(dedent("""\
                ---
                version: 0.2
                text: rst
                fix_inline_single_backquotes: true
                # post: pdf
                --- |
                """))  # NOQA
                fp.write(rst.update_sections())

    def roundtrip(self) -> None:
        for file_name in self._todo():
            self.round_trip_one(file_name)

    def round_trip_one(self, path: Path) -> None:
        from ._convertor.roundtrip import RoundTripConvertor

        self._current_path = path
        if self._args.verbose > 0:
            self.name()
        yaml = YAML()
        convertor = None
        for x in yaml.load_all(path):
            if convertor is None:
                convertor = RoundTripConvertor(self, yaml, x, path)
                continue
            convertor(x)
        assert convertor is not None
        if convertor.updated:
            convertor.write()


##############################################################################

DOCEM = b'...'
DIREM = b'---'
bNEWLINE = 10
bSPACE = ord(' ')
bTAB = ord('\t')


class YamlDocStreamSplitter:
    """
    split a YAML document stream into one or more  documents.

    The stream is read in memory as bytes.
    A document starts:
    - at the beginning of the stream,
    - after a `...` (document end marker)
    - starting with `---` (directives end marker) if not preceded by
      only directives, empty lines or comments.
    directives must start with '%' in first position of line
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._content = path.read_bytes()
        self._indices: List[Tuple[int, int]] = []

    def indices(self) -> Any:
        if self._indices:
            for x in self._indices:
                yield x
            return
        content = self._content
        content_len = len(content)
        index = 0
        newline = True
        check_directive = True
        prev = 0
        while index < content_len:
            if not newline:
                newline = content[index] == 10
                index += 1
                continue
            # print('check directive', check_directive, index, content[index:index+20])
            if check_directive:
                newline = False
                if content[index] == ord('%'):
                    index += 1
                    while index < content_len:
                        index += 1
                        if content[index] == 10:
                            break
                    newline = True
                    index += 1
                    continue
                # check if this line is empty or starts with a comment
                ti = index
                while check_directive and ti < content_len:
                    if content[ti] == bNEWLINE:
                        index = ti
                        newline = True
                        break
                    if content[ti] in (bSPACE, bTAB):
                        ti += 1
                        continue
                    if content[ti] == ord('#'):
                        # found a comment, skip to end of line
                        # print('found comment', content[ti:ti+20])
                        index = ti + 1
                        while index < content_len:
                            index += 1
                            if content[index] == 10:
                                break
                        newline = True
                        break
                    # print('unsetting directive', index)
                    check_directive = False
                    newline = False
            if not newline:
                # print('unset newline')
                continue
            # print('check directive2', check_directive, index)
            if (
                content[index : index + 3] == DOCEM
                and content[index + 3 : index + 4] in b'\n \t'
            ):
                check_directive = True
                if content[index + 3] == 10:
                    index += 4
                    # print('setting directive nl', content[index:index+20], newline)
                    self._indices.append((prev, index))
                    yield prev, index  # ToDo check if only when not check_directive
                    prev = index
                    # newline = True  # is already True, otherwise we wouldn't check for DOCEM
                else:
                    index += 3
                    # print('setting directive sp', content[index:index+20], newline)
                    self._indices.append((prev, index))
                    yield prev, index  # ToDo check if only when not check_directive
                    prev = index
                    newline = False
                    continue
            # the following also recognizes a --- without newline at the end
            # of a file, as then content[3:3] is empty and part of any string
            if (
                content[index : index + 3] == DIREM
                and content[index + 3 : index + 4] in b'\n \t'
            ):
                # print('ending directive', check_directive, content[index:index+20])
                if not check_directive:
                    self._indices.append((prev, index))
                    yield prev, index
                    prev = index
                else:
                    check_directive = False
                index += 3
            newline = content[index] == 10
            index += 1
        self._indices.append((prev, content_len))
        yield prev, content_len

    def __iter__(self) -> Any:
        return YamlDocStreamIterator(self)

    def iter(self) -> Any:
        return YamlDocStreamIterator(self)


class YamlDocStreamIterator:
    def __init__(self, ys: YamlDocStreamSplitter) -> None:
        self.ys = ys
        self.indices = list(self.ys.indices())
        self.index = 0

    def __next__(self) -> bytes:
        if self.index >= len(self.indices):
            raise StopIteration
        s, e = self.indices[self.index]
        self.index += 1
        return self.ys._content[s:e]

    def next(self, yaml: Optional[YAML] = None) -> Any:
        # returns the bytes of the next document, or data if yaml parsed in
        # an emtpy doc returns None that is not ok.
        try:
            if yaml is None:
                return self.__next__()
            else:
                return yaml.load(self.__next__())
        except StopIteration:
            return None

    def skip(self) -> None:
        # skip a document
        self.index += 1

    def done(self) -> bool:
        return self.index > len(self.indices)
