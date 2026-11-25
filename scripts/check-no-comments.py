#!/usr/bin/env python3
import argparse
import fnmatch
import io
import os
import re
import subprocess
import sys
import tokenize
from bisect import bisect_right
from pathlib import Path

MESSAGE = "comment found"

ALLOWED_DIRECTIVES = (
    r"noqa\b",
    r"type:\s*ignore",
    r"pragma\b",
    r"pylint:",
    r"fmt:\s*(?:off|on|skip)\b",
    r"isort:",
    r"ruff:",
    r"mypy:",
    r"eslint-",
    r"prettier-ignore",
    r"@ts-expect-error",
    r"@ts-ignore",
    r"@ts-nocheck",
    r"<reference\b",
    r"tflint-ignore",
    r"checkov:skip",
    r"shellcheck\b",
    r"yamllint\b",
    r"hadolint\b",
    r"(?:syntax|escape|check)=",
    r"@license",
    r"Copyright",
    r"SPDX-License-Identifier",
    r"(?:istanbul|c8|v8)\s+ignore",
    r"webpackChunkName",
    r"sourceMappingURL",
)

ALLOWED_RE = re.compile("|".join(ALLOWED_DIRECTIVES))
ENCODING_RE = re.compile(r"coding[:=]\s*[-\w.]+")
JS_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
JSX_SUFFIXES = {".tsx", ".jsx"}
HCL_SUFFIXES = {".tf", ".tfvars", ".hcl"}
SHELL_SUFFIXES = {".sh", ".bash"}
YAML_SUFFIXES = {".yml", ".yaml"}
IGNORED_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
REGEX_PRECEDERS = frozenset("(,=:[!&|?{};+-*%<>~^")
REGEX_KEYWORDS = frozenset(
    "return typeof instanceof in of new delete void throw case do else yield await".split()
)
WORD_RE = re.compile(r"[A-Za-z0-9_$\u0080-\uffff]+")
HCL_HEREDOC_RE = re.compile(r"<<-?([A-Za-z_]\w*)[ \t]*\r?$", re.MULTILINE)
SHELL_HEREDOC_RE = re.compile(r"<<-?[ \t]*(?:'([^']+)'|\"([^\"]+)\"|\\?([A-Za-z_]\w*))")
YAML_BLOCK_RE = re.compile(r"(?:^|[:\-]\s+|\s[&!]\S+\s+)[|>][+\-0-9]*$")


class ScanError(Exception):
    pass


class LineIndex:
    def __init__(self, text):
        self.newlines = [m.start() for m in re.finditer("\n", text)]

    def line(self, pos):
        return bisect_right(self.newlines, pos) + 1


def skip_quoted(text, pos, quote, escapes):
    while pos < len(text):
        char = text[pos]
        if escapes and char == "\\":
            pos += 2
        elif char == quote:
            return pos + 1
        else:
            pos += 1
    return len(text)


def skip_heredoc_body(text, pos, tag):
    while pos < len(text):
        end = text.find("\n", pos)
        end = len(text) if end < 0 else end
        line = text[pos:end]
        pos = end + 1
        if line.strip() == tag:
            break
    return pos


class BaseScanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.size = len(text)
        self.index = LineIndex(text)
        self.found = []

    def record(self, start, end):
        self.found.append((self.index.line(start), self.text[start:end]))

    def line_comment(self):
        end = self.text.find("\n", self.pos)
        end = self.size if end < 0 else end
        self.record(self.pos, end)
        self.pos = end

    def block_comment(self):
        end = self.text.find("*/", self.pos + 2)
        end = self.size if end < 0 else end + 2
        self.record(self.pos, end)
        self.pos = end


class JsScanner(BaseScanner):
    def __init__(self, text, jsx):
        super().__init__(text)
        self.jsx = jsx

    @staticmethod
    def regex_allowed(prev):
        return prev == "" or prev in REGEX_PRECEDERS or prev in REGEX_KEYWORDS

    def skip_regex(self):
        text = self.text
        self.pos += 1
        in_class = False
        while self.pos < self.size:
            char = text[self.pos]
            if char == "\\":
                self.pos += 2
                continue
            if char == "\n":
                return
            self.pos += 1
            if char == "[":
                in_class = True
            elif char == "]":
                in_class = False
            elif char == "/" and not in_class:
                break
        while self.pos < self.size and text[self.pos].isalpha():
            self.pos += 1

    def skip_template(self):
        text = self.text
        self.pos += 1
        while self.pos < self.size:
            if text[self.pos] == "\\":
                self.pos += 2
            elif text[self.pos] == "`":
                self.pos += 1
                return
            elif text.startswith("${", self.pos):
                self.pos += 2
                self.code(True)
                self.pos += 1
            else:
                self.pos += 1

    def jsx_tag(self):
        text = self.text
        closing = text[self.pos + 1 : self.pos + 2] == "/"
        self_closing = False
        self.pos += 1
        while self.pos < self.size:
            char = text[self.pos]
            if char in "\"'":
                end = text.find(char, self.pos + 1)
                self.pos = self.size if end < 0 else end + 1
            elif char == "{":
                self.pos += 1
                self.code(True)
                self.pos += 1
            elif char == ">":
                self_closing = text[self.pos - 1] == "/"
                self.pos += 1
                break
            else:
                self.pos += 1
        if closing:
            return "close"
        return "self" if self_closing else "open"

    def jsx_element(self):
        text = self.text
        depth = 0
        while self.pos < self.size:
            kind = self.jsx_tag()
            if kind == "open":
                depth += 1
            elif kind == "close":
                depth -= 1
            if depth <= 0:
                return
            while self.pos < self.size and text[self.pos] != "<":
                if text[self.pos] == "{":
                    self.pos += 1
                    self.code(True)
                    self.pos += 1
                else:
                    self.pos += 1

    def code(self, stop_at_brace=False):
        text = self.text
        prev = ""
        depth = 0
        while self.pos < self.size:
            char = text[self.pos]
            pair = text[self.pos : self.pos + 2]
            if char.isspace():
                self.pos += 1
            elif pair == "//":
                self.line_comment()
            elif pair == "/*":
                self.block_comment()
            elif char in "\"'":
                self.pos = skip_quoted(text, self.pos + 1, char, True)
                prev = "x"
            elif char == "`":
                self.skip_template()
                prev = "x"
            elif char == "/":
                if self.regex_allowed(prev):
                    self.skip_regex()
                    prev = "x"
                else:
                    self.pos += 1
                    prev = "/"
            elif (
                self.jsx
                and char == "<"
                and self.regex_allowed(prev)
                and re.match(r"[A-Za-z>]", text[self.pos + 1 : self.pos + 2])
            ):
                self.jsx_element()
                prev = "x"
            else:
                word = WORD_RE.match(text, self.pos)
                if word:
                    prev = word.group()
                    self.pos = word.end()
                    continue
                if char == "{":
                    depth += 1
                elif char == "}":
                    if stop_at_brace and depth == 0:
                        return
                    depth = max(depth - 1, 0)
                prev = char
                self.pos += 1


class CssScanner(BaseScanner):
    def __init__(self, text, scss):
        super().__init__(text)
        self.scss = scss

    def code(self):
        text = self.text
        while self.pos < self.size:
            char = text[self.pos]
            pair = text[self.pos : self.pos + 2]
            if pair == "/*":
                self.block_comment()
            elif self.scss and pair == "//":
                self.line_comment()
            elif char in "\"'":
                self.pos = skip_quoted(text, self.pos + 1, char, True)
            elif char in "uU" and text[self.pos : self.pos + 4].lower() == "url(":
                start = self.pos + 4
                while start < self.size and text[start] in " \t":
                    start += 1
                if text[start : start + 1] in ("'", '"'):
                    self.pos += 4
                else:
                    end = text.find(")", start)
                    self.pos = self.size if end < 0 else end + 1
            else:
                self.pos += 1


class HclScanner(BaseScanner):
    def string(self):
        text = self.text
        self.pos += 1
        while self.pos < self.size:
            char = text[self.pos]
            if char == "\\":
                self.pos += 2
            elif char == '"':
                self.pos += 1
                return
            elif char == "\n":
                return
            elif text.startswith(("$${", "%%{"), self.pos):
                self.pos += 3
            elif text.startswith(("${", "%{"), self.pos):
                self.pos += 2
                self.code(True)
                self.pos += 1
            else:
                self.pos += 1

    def code(self, stop_at_brace=False):
        text = self.text
        depth = 0
        while self.pos < self.size:
            char = text[self.pos]
            pair = text[self.pos : self.pos + 2]
            if char == '"':
                self.string()
            elif char == "#" or pair == "//":
                self.line_comment()
            elif pair == "/*":
                self.block_comment()
            elif pair == "<<" and HCL_HEREDOC_RE.match(text, self.pos):
                tag = HCL_HEREDOC_RE.match(text, self.pos).group(1)
                eol = text.find("\n", self.pos)
                self.pos = self.size if eol < 0 else skip_heredoc_body(text, eol + 1, tag)
            else:
                if char == "{":
                    depth += 1
                elif char == "}":
                    if stop_at_brace and depth == 0:
                        return
                    depth = max(depth - 1, 0)
                self.pos += 1


class ShellScanner(BaseScanner):
    def __init__(self, text):
        super().__init__(text)
        self.pending = []

    def word_start(self):
        return self.pos == 0 or self.text[self.pos - 1] in " \t\r\n;&|()"

    def skip_braces(self):
        text = self.text
        self.pos += 2
        depth = 1
        while self.pos < self.size and depth:
            char = text[self.pos]
            if char == "\\":
                self.pos += 2
                continue
            if char in "'\"":
                self.pos = skip_quoted(text, self.pos + 1, char, char == '"')
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            self.pos += 1

    def dollar(self):
        text = self.text
        following = text[self.pos + 1 : self.pos + 2]
        if following == "{":
            self.skip_braces()
        elif following == "'":
            self.pos = skip_quoted(text, self.pos + 2, "'", True)
        elif following == "(":
            self.pos += 2
            self.code(True)
            self.pos += 1
        elif following and following in "#?$!@*-0123456789_":
            self.pos += 2
        else:
            self.pos += 1

    def double_quoted(self):
        text = self.text
        self.pos += 1
        while self.pos < self.size:
            char = text[self.pos]
            if char == "\\":
                self.pos += 2
            elif char == '"':
                self.pos += 1
                return
            elif char == "$":
                self.dollar()
            elif char == "`":
                self.pos = skip_quoted(text, self.pos + 1, "`", True)
            else:
                self.pos += 1

    def heredoc_tag(self):
        if self.text.startswith("<<<", self.pos):
            self.pos += 3
            return
        match = SHELL_HEREDOC_RE.match(self.text, self.pos)
        if match:
            self.pending.append(next(group for group in match.groups() if group))
            self.pos = match.end()
        else:
            self.pos += 2

    def newline(self):
        self.pos += 1
        for tag in self.pending:
            self.pos = skip_heredoc_body(self.text, self.pos, tag)
        self.pending = []

    def code(self, closer=False):
        text = self.text
        depth = 0
        while self.pos < self.size:
            char = text[self.pos]
            if char == "\\":
                self.pos += 2
            elif char == "'":
                self.pos = skip_quoted(text, self.pos + 1, "'", False)
            elif char == '"':
                self.double_quoted()
            elif char == "`":
                self.pos = skip_quoted(text, self.pos + 1, "`", True)
            elif char == "$":
                self.dollar()
            elif char == "#" and self.word_start():
                self.line_comment()
            elif char == "<" and text.startswith("<<", self.pos):
                self.heredoc_tag()
            elif char == "\n":
                self.newline()
            elif closer and char == "(":
                depth += 1
                self.pos += 1
            elif closer and char == ")":
                if depth == 0:
                    return
                depth -= 1
                self.pos += 1
            else:
                self.pos += 1


def scan_python(text):
    try:
        return [
            (token.start[0], token.string)
            for token in tokenize.generate_tokens(io.StringIO(text).readline)
            if token.type == tokenize.COMMENT
        ]
    except (tokenize.TokenError, SyntaxError) as error:
        raise ScanError(f"cannot tokenize: {error}") from error


def scan_js(text, jsx):
    scanner = JsScanner(text, jsx)
    scanner.code()
    return scanner.found


def scan_css(text, scss):
    scanner = CssScanner(text, scss)
    scanner.code()
    return scanner.found


def scan_hcl(text):
    scanner = HclScanner(text)
    scanner.code()
    return scanner.found


def scan_shell(text):
    scanner = ShellScanner(text)
    scanner.code()
    return scanner.found


def yaml_comment_start(line, quote):
    for position, char in enumerate(line):
        before = line[position - 1] if position else " "
        if quote:
            if char == "\\" and quote == '"':
                continue
            if char == quote and not (quote == '"' and before == "\\"):
                quote = ""
        elif char in "\"'" and before in " \t:-[{,":
            quote = char
        elif char == "#" and before in " \t":
            return position, quote
    return -1, quote


def scan_yaml(text):
    found = []
    quote = ""
    block_indent = None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if block_indent is not None:
            if not stripped or indent > block_indent:
                continue
            block_indent = None
        start, quote = yaml_comment_start(line, quote)
        if start >= 0:
            found.append((number, line[start:].rstrip()))
        content = line if start < 0 else line[:start]
        if not quote and YAML_BLOCK_RE.search(content.rstrip()):
            block_indent = indent
    return found


def scan_dockerfile(text):
    return [
        (number, line.strip())
        for number, line in enumerate(text.splitlines(), 1)
        if line.lstrip().startswith("#")
    ]


def scanner_for(path):
    name = path.name
    suffix = path.suffix.lower()
    if name.startswith("Dockerfile") or name.endswith(".Dockerfile"):
        return scan_dockerfile
    if suffix == ".py":
        return scan_python
    if suffix in JS_SUFFIXES:
        return lambda text: scan_js(text, suffix in JSX_SUFFIXES)
    if suffix in {".css", ".scss"}:
        return lambda text: scan_css(text, suffix == ".scss")
    if suffix in HCL_SUFFIXES:
        return scan_hcl
    if suffix in SHELL_SUFFIXES:
        return scan_shell
    if suffix in YAML_SUFFIXES:
        return scan_yaml
    return None


def is_allowed(line, text):
    if line == 1 and text.startswith("#!"):
        return True
    if line <= 2 and ENCODING_RE.search(text):
        return True
    return bool(ALLOWED_RE.match(text.lstrip("/*#! \t")))


def scan_file(path):
    path = Path(path)
    scanner = scanner_for(path)
    if scanner is None:
        return []
    try:
        text = path.read_bytes().decode("utf-8-sig")
    except (OSError, UnicodeDecodeError) as error:
        raise ScanError(f"cannot read: {error}") from error
    try:
        return [(line, text) for line, text in scanner(text) if not is_allowed(line, text)]
    except RecursionError as error:
        raise ScanError("nesting too deep") from error


def git_files():
    result = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, check=True, text=True
    )
    return [name for name in result.stdout.split("\0") if name]


def expand(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for root, dirs, files in os.walk(path):
                dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
                for name in sorted(files):
                    yield Path(root, name).as_posix()
        else:
            yield path.as_posix()


def is_excluded(path, patterns):
    name = path.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(name, p) for p in patterns)


def format_finding(path, line, output_format, warn_only):
    if output_format == "github":
        level = "warning" if warn_only else "error"
        return f"::{level} file={path},line={line}::{MESSAGE}"
    return f"{path}:{line}: {MESSAGE}"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="check-no-comments.py",
        description="Report comments that are not allowed tool directives (GEN-CMT-001).",
    )
    parser.add_argument("--warn-only", action="store_true", help="always exit 0")
    parser.add_argument("--format", choices=("text", "github"), default="text")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB")
    parser.add_argument("paths", nargs="*", metavar="PATH")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.paths:
        missing = [p for p in args.paths if not Path(p).exists()]
        if missing:
            print(f"error: path not found: {', '.join(missing)}", file=sys.stderr)
            return 2
        candidates = list(expand(args.paths))
    else:
        try:
            candidates = git_files()
        except (OSError, subprocess.CalledProcessError) as error:
            print(f"error: cannot list files with git: {error}", file=sys.stderr)
            return 2
    total = 0
    for path in candidates:
        if is_excluded(path, args.exclude):
            continue
        try:
            findings = scan_file(path)
        except ScanError as error:
            print(f"warning: {path}: {error}", file=sys.stderr)
            continue
        for line, _ in findings:
            print(format_finding(path, line, args.format, args.warn_only))
        total += len(findings)
    return 1 if total and not args.warn_only else 0


if __name__ == "__main__":
    sys.exit(main())
