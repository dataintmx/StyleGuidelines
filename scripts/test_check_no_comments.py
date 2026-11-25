import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name("check-no-comments.py")
spec = importlib.util.spec_from_file_location("check_no_comments", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def lines_found(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return [line for line, _ in check.scan_file(path)]


POSITIVE = [
    ("a.py", "x = 1\n# note\ny = 2  # trailing\n", [2, 3]),
    ("a.ts", "const a = 1; // note\n/* block\nmore */\nconst b = 2;\n", [1, 2]),
    ("a.tsx", "const a = <div>{/* note */}</div>;\n", [1]),
    ("a.js", "const t = `${a /* in */}`;\n", [1]),
    ("a.css", "a { color: red; } /* note */\n", [1]),
    ("a.scss", "a { color: red; } // note\n", [1]),
    ("a.tf", 'a = 1 # one\nb = 2 // two\n/* three */\n', [1, 2, 3]),
    ("a.sh", "echo hi # note\n# note\n", [1, 2]),
    ("a.yaml", "a: 1 # note\n# note\n", [1, 2]),
    ("Dockerfile", "FROM x\n# note\n", [2]),
    ("base.Dockerfile", "FROM x\n  # note\n", [2]),
]


@pytest.mark.parametrize(("name", "content", "expected"), POSITIVE)
def test_reports_comments(tmp_path, name, content, expected):
    assert lines_found(tmp_path, name, content) == expected


NEGATIVE = [
    ("a.py", 'def f():\n    """Doc."""\n    return "# not"\n'),
    ("a.py", "x = '''\n# inside\n'''\n"),
    ("a.ts", 'const u = "http://x.y"; const v = \'//z\';\n'),
    ("a.ts", "const r = /\\/\\/[/]#/g; const d = a / b / c;\n"),
    ("a.ts", "const t = `http://${a}/${`//${b}`}`;\n"),
    ("a.tsx", 'const a = <a href="http://x.y">http://x.y</a>;\n'),
    ("a.jsx", "const a = <p>{x} // text</p>;\n"),
    ("a.css", "a { background: url(http://x.y/a.png); content: '/* x */'; }\n"),
    ("a.scss", "a { background: url(//cdn.x/a.png); }\n"),
    ("a.tf", 'a = "http://x#y"\nb = "${var.a == "#" ? "//" : "/*"}"\n'),
    ("a.tf", 'a = <<EOT\n# not\n// not\nEOT\nb = 1\n'),
    ("a.tf", 'a = <<-EOT\n  # not\n  EOT\n'),
    ("a.sh", "echo 'a # b' \"c # d\" a#b\n"),
    ("a.sh", 'n=${#x}; m=$#; echo "$#" ${x#pre}\n'),
    ("a.sh", "cat <<EOF\n# not\nEOF\ncat <<'EOF'\n# not\nEOF\n"),
    ("a.sh", 'echo "$(echo "# x")"\n'),
    ("a.yml", "a: 'x # y'\nb: \"x # y\"\nc: http://x#y\n"),
    ("a.yml", "a: |\n  # text\n  more\nb: >-\n  # text\nc: 1\n"),
    ("a.yml", "- |\n  # text\n- x\n"),
    ("Dockerfile", "FROM x\nRUN echo a # b\n"),
    ("notes.txt", "# anything\n"),
    ("a.md", "<!-- x -->\n"),
]


@pytest.mark.parametrize(("name", "content"), NEGATIVE)
def test_ignores_non_comments(tmp_path, name, content):
    assert lines_found(tmp_path, name, content) == []


def test_comment_after_heredoc_and_block_is_found(tmp_path):
    assert lines_found(tmp_path, "a.sh", "cat <<EOF\n# no\nEOF\n# yes\n") == [4]
    assert lines_found(tmp_path, "a.yml", "a: |\n  x\n# yes\nb: 1\n") == [3]
    assert lines_found(tmp_path, "a.tsx", "const a = <p>x</p>; // yes\n") == [1]


ALLOWED = [
    ("a.py", "#!/usr/bin/env python3\n"),
    ("a.py", "# -*- coding: utf-8 -*-\n"),
    ("a.py", "# vim: set fileencoding=utf-8 :\n"),
    ("a.py", "x = 1  # noqa: E501\n"),
    ("a.py", "x = 1  # type: ignore[attr-defined]\n"),
    ("a.py", "x = 1  # pragma: no cover\n"),
    ("a.py", "x = 1  # pylint: disable=all\n"),
    ("a.py", "# fmt: off\n# fmt: on\nx = 1  # fmt: skip\n"),
    ("a.py", "# isort: skip_file\n"),
    ("a.py", "x = 1  # ruff: noqa\n"),
    ("a.py", "x = 1  # mypy: ignore-errors\n"),
    ("a.py", "# Copyright 2026 DataInt\n# SPDX-License-Identifier: MIT\n"),
    ("a.ts", "// eslint-disable-next-line no-console\n"),
    ("a.ts", "/* eslint-disable no-console */\n"),
    ("a.ts", "// prettier-ignore\n"),
    ("a.ts", "// @ts-expect-error x\n// @ts-ignore\n// @ts-nocheck\n"),
    ("a.ts", '/// <reference types="node" />\n'),
    ("a.ts", "/** @license MIT */\n/*! Copyright 2026 */\n"),
    ("a.ts", "/* istanbul ignore next */\n/* c8 ignore start */\n// v8 ignore next\n"),
    ("a.ts", 'const m = import(/* webpackChunkName: "x" */ "./x");\n'),
    ("a.js", "//# sourceMappingURL=a.js.map\n"),
    ("a.tsx", "const a = <div>{/* eslint-disable-line */}</div>;\n"),
    ("a.tf", "a = 1 # tflint-ignore: terraform_unused_declarations\n"),
    ("a.tf", "# checkov:skip=CKV_AWS_1: reason\n"),
    ("a.sh", "#!/usr/bin/env bash\n# shellcheck disable=SC2086\n"),
    ("a.yml", "# yamllint disable-line rule:line-length\n"),
    ("Dockerfile", "# syntax=docker/dockerfile:1\n# escape=`\n# check=skip=all\n"),
    ("Dockerfile", "FROM x\n# hadolint ignore=DL3008\n"),
]


@pytest.mark.parametrize(("name", "content"), ALLOWED)
def test_allows_directives(tmp_path, name, content):
    assert lines_found(tmp_path, name, content) == []


def test_shebang_only_on_first_line(tmp_path):
    assert lines_found(tmp_path, "a.sh", "echo\n#!/bin/sh\n") == [2]


def test_unterminated_python_warns_and_continues(tmp_path, capsys):
    bad = tmp_path / "bad.py"
    bad.write_text("x = (\n", encoding="utf-8")
    good = tmp_path / "good.py"
    good.write_text("# note\n", encoding="utf-8")
    undecodable = tmp_path / "bin.sh"
    undecodable.write_bytes(b"\xff\xfe\n")
    code = check.main([str(bad), str(undecodable), str(good)])
    captured = capsys.readouterr()
    assert code == 1
    assert f"{good}:1: comment found" in captured.out
    assert "bad.py" in captured.err
    assert "bin.sh" in captured.err


def test_exit_codes_and_text_format(tmp_path, capsys):
    dirty = tmp_path / "a.py"
    dirty.write_text("# note\n", encoding="utf-8")
    clean = tmp_path / "b.py"
    clean.write_text("x = 1\n", encoding="utf-8")
    assert check.main([str(clean)]) == 0
    assert check.main([str(dirty)]) == 1
    assert capsys.readouterr().out.splitlines()[-1] == f"{dirty}:1: comment found"
    assert check.main(["--warn-only", str(dirty)]) == 0


def test_usage_errors_exit_two(tmp_path):
    with pytest.raises(SystemExit) as raised:
        check.main(["--format", "xml"])
    assert raised.value.code == 2
    assert check.main([str(tmp_path / "missing.py")]) == 2


def test_github_format(tmp_path, capsys):
    dirty = tmp_path / "a.py"
    dirty.write_text("x = 1\n# note\n", encoding="utf-8")
    check.main(["--format", "github", str(dirty)])
    assert capsys.readouterr().out.strip() == f"::error file={dirty},line=2::comment found"
    check.main(["--format", "github", "--warn-only", str(dirty)])
    assert capsys.readouterr().out.strip() == f"::warning file={dirty},line=2::comment found"


def test_excludes_by_glob_and_basename(tmp_path):
    (tmp_path / "keep").mkdir()
    (tmp_path / "skip").mkdir()
    (tmp_path / "keep" / "a.py").write_text("# x\n", encoding="utf-8")
    (tmp_path / "skip" / "b.py").write_text("# x\n", encoding="utf-8")
    (tmp_path / "keep" / "gen.py").write_text("# x\n", encoding="utf-8")
    argv = ["--exclude", "*/skip/*", "--exclude", "gen.py", str(tmp_path)]
    assert check.main(argv) == 1
    argv.extend(["--exclude", "*/keep/a.py"])
    assert check.main(argv) == 0


def test_default_paths_come_from_git(tmp_path, monkeypatch, capsys):
    dirty = tmp_path / "a.py"
    dirty.write_text("# x\n", encoding="utf-8")
    monkeypatch.setattr(check, "git_files", lambda: [str(dirty), str(tmp_path / "b.md")])
    assert check.main([]) == 1
    assert capsys.readouterr().out == f"{dirty}:1: comment found\n"


@pytest.mark.parametrize("path", [SCRIPT, Path(__file__)])
def test_script_and_tests_pass_their_own_check(path):
    assert check.scan_file(path) == []
