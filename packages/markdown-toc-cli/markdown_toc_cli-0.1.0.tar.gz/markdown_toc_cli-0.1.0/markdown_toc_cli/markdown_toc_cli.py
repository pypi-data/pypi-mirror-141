"""
Generate a table of contents for a markdown file, optionally inserting it between
<!-- toc -->
<!-- tocstop -->
"""
from __future__ import annotations

import argparse
import re
import shlex
from typing import Sequence

import mistletoe

VERSION = "0.1.0"

COMMENT_PREFIX = "<!-- markdown-toc-cli"


class Heading:
    """Used to parse and render individual headings"""

    def __init__(self, heading_obj):
        self.level = heading_obj.level
        self.heading_obj = heading_obj
        self.text = self.render_heading_text(heading_obj)
        self.link = self.render_link(self.text)

    @staticmethod
    def render_heading_text(heading_obj):
        """generate the text for a heading from all it's child objects"""
        return "".join(map(Heading.render_child, heading_obj.children))

    @staticmethod
    def render_child(child):
        """render a single child object"""
        if isinstance(child, mistletoe.span_token.RawText):
            return child.content
        if isinstance(child, mistletoe.span_token.InlineCode):
            return f"`{child.children[0].content}`"
        raise ValueError(f"Unknown child type: {child}")

    @staticmethod
    def render_link(text):
        """generate GFM link from text"""
        # convert spaces go to hyphens (other whitespace is removed below)
        link = text.lower().replace(" ", "-")
        # non-alphanumeric/underscore/hyphen is removed
        link = re.sub(r"[^\w_-]", "", link)
        return f"[{text}](#{link})"

    def __str__(self):
        return f"{'#' * self.level} {self.text}"

    def toc_entry(self, prefix, indentation, minlevel, maxlevel):
        """generate a table of contents entry"""
        level_offset = minlevel
        if self.level > maxlevel:
            return ""
        if self.level < minlevel:
            return ""
        indentation = indentation * (self.level - level_offset)
        return f"{indentation}{prefix}{self.link}"


def render_toc(headings, prefix, indentation, minlevel, maxlevel):
    """generate a table of contents from a list of headings"""
    return "\n".join(
        filter(
            None,
            [
                heading.toc_entry(prefix, indentation, minlevel, maxlevel)
                for heading in headings
            ],
        )
    )


def insert_toc(filename, toc):
    """insert a table of contents into a markdown file"""
    with open(filename, encoding="utf-8") as infile:
        lines = infile.readlines()

    # find the insertion point
    toc_start = next(
        (i for i, v in enumerate(lines) if v.startswith(COMMENT_PREFIX)), None
    )
    toc_end = next(
        (i for i, v in enumerate(lines) if v.startswith(f"{COMMENT_PREFIX}-end")), None
    )

    if not toc_start:
        return

    if not toc_end:
        toc += f"\n\n{COMMENT_PREFIX}-end -->"
        toc_end = toc_start + 1

    lines_out = lines[: toc_start + 1] + ["\n"] + [toc] + ["\n\n"] + lines[toc_end:]

    with open(filename, "w", encoding="utf-8") as outfile:
        outfile.write("".join(lines_out))


def generate_toc(filename, prefix, indentation, minlevel, maxlevel):
    """generate a table of contents from a markdown file"""
    with open(filename, encoding="utf-8") as infile:
        doc = mistletoe.Document(infile.read())
        headings = filter(
            lambda x: isinstance(x, mistletoe.block_token.Heading), doc.children
        )
        toc = render_toc(
            [Heading(h) for h in headings], prefix, indentation, minlevel, maxlevel
        )

    insert_toc(filename, toc)


def parse_comment_args(comment):
    """parse the toc comment arguments from a markdown file"""
    args = {}
    for arg in shlex.split(comment):
        if "=" in arg:
            key, value = arg.split("=")
            key = key.strip("-")
            args[key] = value

    return args


def get_args(filename):
    """get the toc comment arguments from a markdown file"""
    # defaults
    args = {"prefix": "- ", "indentation": "  ", "minlevel": 1, "maxlevel": 6}
    with open(filename, encoding="utf-8") as infile:
        for line in infile.readlines():
            if line.startswith(COMMENT_PREFIX):
                # update with any settings
                args.update(parse_comment_args(line))

    args["minlevel"] = int(args["minlevel"])
    args["maxlevel"] = int(args["maxlevel"])

    return args


def main(argv: Sequence[str] | None = None) -> int:
    """main function"""
    parser = argparse.ArgumentParser(
        description=(
            "Inserts a table of contents into one or more markdown files.\n\nThe table"
            f" of contents is inserted right after the {COMMENT_PREFIX} --> comment in"
            " the documents. The TOC is formatted according to the"
            f" {COMMENT_PREFIX} --> arguments, all optional (defaults shown):"
            f" {COMMENT_PREFIX} --prefix='- ' --indentation='  ' --minlevel=1"
            " --maxlevel=6 -->"
        )
    )
    parser.add_argument(
        "--version", "-v", action="version", version="%(prog)s " + VERSION
    )
    parser.add_argument("FILENAMES", nargs="*")

    args = parser.parse_args(argv)

    for filename in args.FILENAMES:

        comment_args = get_args(filename)
        generate_toc(filename, **comment_args)
    return 0


if __name__ == "__main__":
    SystemExit(main())
