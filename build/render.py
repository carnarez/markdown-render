"""Template script to render Markdown to HTML."""

import os
import re
import sys
import typing

import yaml

from jinja2 import Environment, BaseLoader, Template
from markdown import markdown
from markdown.extensions import Extension
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.md_in_html import MarkdownInHtmlExtension
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
from yaml import Loader

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

# raw markdown content
with open(sys.argv[1]) as f:
    text = f.read().strip()

# preprocess: extract front matter
meta: typing.Dict[str, typing.Any] = {}
rgxp: re.Pattern = re.compile(r"^---\n(.+?)\n---\n\n", flags=re.DOTALL)
if text.startswith("---\n"):
    try:
        meta = yaml.load(re.match(rgxp, text).group(1), Loader=Loader)
        text = re.sub(rgxp, "", text, count=1).strip()
    except AttributeError:
        pass

# preprocess: generate metadata if undefined
if "title" not in meta:
    meta["title"] = re.sub(".md$", "", sys.argv[1].split("/")[-2].capitalize())

# process: convert the markdown
html: str = markdown(text, extensions=exts)

# postprocess: escape mermaid code blocks
html = re.sub(
    '(<div class="mermaid">.*?</div>)',
    r"<!-- htmlmin:ignore -->\n<!-- prettier-ignore -->\n\1\n<!-- htmlmin:ignore -->",
    html,
    flags=re.DOTALL,
)

# render template/output to stdout and log to stderr
sys.stdout.write(tmpl.render(content=html, **meta))
sys.stderr.write(f'{sys.argv[1].lstrip("./")}\n')
