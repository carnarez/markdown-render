"""Template script to render Markdown to HTML."""

import os
import re
import sys
import typing

from jinja2 import Environment, BaseLoader, Template
from markdown import Markdown

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

# jinja2 template
jenv: Environment = Environment(loader=BaseLoader())
try:
    tmpl: Template = jenv.from_string(open(sys.argv[2]).read())
except IndexError:
    tmpl: Template = jenv.from_string(open("template.html").read())

# process the markdown
mkdw: Markdown = Markdown(extensions=exts)
html: str = mkdw.convert(open(sys.argv[1]).read())
meta: typing.Dict[str, str] = {k: " ".join(v) for k, v in mkdw.Meta.items()}

# postprocess: escape mermaid code blocks
html = re.sub(
    '(<div class="mermaid">.*?</div>)',
    r"<!-- htmlmin:ignore -->\n<!-- prettier-ignore -->\n\1\n<!-- htmlmin:ignore -->",
    html,
    flags=re.DOTALL,
)

# postprocess: generate metadata if undefined
if "title" not in meta:
    meta["title"] = re.sub(".md$", "", sys.argv[1].split("/")[-2].capitalize())

# render template/output to stdout and log to stderr
sys.stdout.write(tmpl.render(content=html, **meta))
sys.stderr.write(f'{sys.argv[1].lstrip("./")}\n')
