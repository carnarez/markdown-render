"""Template script to render Markdown to HTML."""

import os
import re
import sys
import typing

from markdown import markdown
from markdown.extensions import Extension
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.md_in_html import MarkdownInHtmlExtension
from markdown.extensions.meta import MetaExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown_astdocs import AstdocsExtension
from markdown_img import ImgExtension
from markdown_insert import InsertExtension
from markdown_script import ScriptExtension
from pymdownx.caret import InsertSupExtension
from pymdownx.emoji import EmojiExtension, gemoji
from pymdownx.highlight import HighlightExtension
from pymdownx.superfences import SuperFencesCodeExtension, fence_div_format
from pymdownx.tilde import DeleteSubExtension

# check extension respective documentations for configuration
exts: typing.List[Extension] = [
    AstdocsExtension(),
    DeleteSubExtension(),
    EmojiExtension(emoji_index=gemoji),
    FootnoteExtension(BACKLINK_TEXT=""),
    HighlightExtension(use_pygments=False),
    ImgExtension(),
    InsertExtension(parent_path=os.path.dirname(os.path.realpath(sys.argv[1]))),
    InsertSupExtension(),
    MarkdownInHtmlExtension(),
    MetaExtension(),
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
html: str = markdown(f"[TOC]\n\n{open(sys.argv[1]).read()}", extensions=exts)

# remove table of contents if empty
html = re.sub(
    r'<div class="toc">\s*?<ul>\s*?</ul>\s*?</div>\s*?', "", html, flags=re.DOTALL
)

# escape mermaid code blocks
html = re.sub(
    '(<div class="mermaid">.*?</div>)',
    r"<!-- htmlmin:ignore -->\n<!-- prettier-ignore -->\n\1\n<!-- htmlmin:ignore -->",
    html,
    flags=re.DOTALL,
)

# chunk of a html template
tmpl: str = open("template.html" if len(sys.argv) < 3 else sys.argv[2]).read()

# render and output
sys.stdout.write(tmpl.replace("%CONTENT%", html).strip())
sys.stderr.write(f'{sys.argv[1].lstrip("./")}\n')
