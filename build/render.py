"""Template script to render Markdown to HTML. Fanciness included."""

import sys
import typing

from markdown import markdown
from markdown.extensions import Extension
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.md_in_html import MarkdownInHtmlExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown_astdocs import AstdocsExtension
from markdown_img import ImgExtension
from markdown_script import ScriptExtension
from pymdownx.caret import InsertSupExtension
from pymdownx.highlight import HighlightExtension
from pymdownx.superfences import SuperFencesCodeExtension, fence_div_format
from pymdownx.tilde import DeleteSubExtension

# check extension respective documentations for configuration
exts: typing.List[Extension] = [
    AstdocsExtension(),
    DeleteSubExtension(),
    FootnoteExtension(),
    HighlightExtension(use_pygments=False),
    ImgExtension(),
    InsertSupExtension(),
    MarkdownInHtmlExtension(),
    ScriptExtension(),
    SuperFencesCodeExtension(
        custom_fences=[
            {"name": "mermaid", "class": "mermaid", "format": fence_div_format}
        ]
    ),
    TableExtension(),
    TocExtension(),
]

# add table of contents
html: str = markdown(f'[TOC]\n\n{open(sys.argv[1]).read()}', extensions=exts)

# chunk of a html template
tmpl: str = open("template.html").read()

print(tmpl.replace("%CONTENT%", html).strip())
