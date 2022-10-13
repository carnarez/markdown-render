"""Template script to render `Markdown` to HTML and index the content for Lunr.

Arguments
---------
--prefix
    Prefix to the output path.
--template
    Path to the HTML template.

Examples
--------
```shell
$ python render.py *.md
$ python render.py --prefix=/var/www *.md
$ python render.py --template=template.html *.md
```
"""

import argparse
import datetime
import io
import json
import os
import re
import xml

from jinja2 import BaseLoader, Environment, Template
from lunr import lunr, get_default_builder
from markdown import Markdown
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
from yaml import Loader, load


def load_template(filepath: str = "./template.html") -> Template:
    """Load the `Jinja2` template.

    Parameters
    ----------
    filepath : str
        Path to the `Jinja2` HTML template. Defaults to `./template.html`.

    Returns
    -------
    : jinja2.Template
        `Jinja2` template ready to be used.
    """
    return Environment(loader=BaseLoader()).from_string(open(filepath).read())


def render_template(root: str, tmpl: Template, meta: dict[str, str], toc: str, html: str) -> str:
    """Render the `Jinja2` template after checking for presence of specific content.

    Parameters
    ----------
    root : str
        Root of the served content.
    tmpl : jinja2.Template
        `Jinja2` template ready to be used.
    meta : dict[str, str]
        Metadata, extracted from the front matter or generated.
    toc : str
        Table of Contents of the converted content.
    html : str
        Generated HTML content.

    Returns
    -------
    : str
        Rendered HTML content.

    Note
    ----
    The current check for equations easily returns false positives.
    """
    return tmpl.render(
        root=root,
        toc=toc,
        content=html,
        highlight=True if '<pre class="highlight">' in html else False,
        katex=True if re.search(r"\$.*\$", html, flags=re.DOTALL) else False,
        lunr=True,  # always true
        mermaid=any(
            [
                True if f'<div class="{m}">' in html else False
                for m in ("mermaid", "naiad")
            ]
        ),
        **meta,
    )


def load_document(filepath: str) -> tuple[dict[str, str], str]:
    """Fetch the `Markdown` content and process present front matter.

    Parameters
    ----------
    filepath : str
        Path to the `Markdown` file.

    Returns
    -------
    : dict[str, str]
        Metadata, extracted from the front matter or generated.
    : str
        Raw `Markdown` content.
    """
    meta: dict[str, str] = {}
    rgxp: re.Pattern = re.compile(r"^---\n(.+?)\n---\n", flags=re.DOTALL)

    # load markdown content
    with open(filepath) as f:
        mdwn = f.read().strip()

    # parse front matter if present
    if mdwn.startswith("---"):
        if (m := re.match(rgxp, mdwn)) is not None:
            meta = load(m.group(1), Loader=Loader)  # type: ignore
            mdwn = re.sub(rgxp, "", mdwn, count=1).strip()

    # generate metadata if undefined
    if "date" not in meta:
        meta["date"] = datetime.date.today().strftime("%Y-%m-%d")

    if "filename" not in meta:
        meta["filename"] = re.sub(".md$", "", filepath.split("/")[-1])

    if "path" not in meta:
        meta["path"] = "/".join(filepath.split("/")[:-1])

    if "title" not in meta:
        meta["title"] = meta["filename"]

    if "url" not in meta:
        cname = os.environ.get("CNAME", "http://localhost:8000").rstrip("/")
        meta["url"] = f'{cname}/{meta["path"]}'

    return meta, mdwn


def clean_document(mdwn: str, ellipsis: str = " [...] ") -> str:
    """Remove `Markdown` syntax from raw content.

    Parameters
    ----------
    mdwn : str
        Raw `Markdown` content to process.
    ellipsis : str
        Text to replace non-indexable content.

    Returns
    -------
    : str
        Cleaned up content.
    """
    # remove toc
    mdwn = mdwn.replace("[TOC]", "")

    # remove footnote markers
    mdwn = re.sub(r"\[\^.+?\]", "", mdwn)

    # remove code blocks
    for p in [f"([`]{{{i}}}.+?[`]{{{i}}})" for i in range(7, 2, -1)]:
        mdwn = re.sub(p, ellipsis, mdwn, flags=re.DOTALL)

    # remove equations
    mdwn = re.sub(r"\${2}[^\$]+?\${2}", ellipsis, mdwn, flags=re.DOTALL)
    mdwn = re.sub(r"\$[^`]+?\$", ellipsis, mdwn)

    # remove special syntax
    mdwn = re.sub(r"!\[.*?\]\(.*?\)", ellipsis, mdwn)
    mdwn = re.sub(r"%\[.*?\]\(.*?\)", ellipsis, mdwn)
    mdwn = re.sub(r"&\[.*?\]\(.*?\)", ellipsis, mdwn)

    # remove html tags
    mdwn = re.sub(r"<.+?>", ellipsis, mdwn)

    # replace title markers
    mdwn = re.sub(r"^[#]+\s*(.*)$", r"%%%SECTION\1%%%PARAGRAPH", mdwn, flags=re.MULTILINE)

    return mdwn


def convert_document(
    mdwn: str,
    extensions: list[Extension],
    output_format: str = "html",
    strip_top_level_tags: bool = True,
) -> tuple[str, str]:
    """Convert the `Markdown` content to supported formats.

    Parameters
    ----------
    mdwn : str
        Raw `Markdown` content to process.
    extensions : list[markdown.extensions.Extension]
        List of [extensions](https://python-markdown.github.io/extensions/) to apply
        during the conversion.
    output_format : str
        Output format after conversion. Note the the patched `markdown.Markdown` object
        supports the `text` conversion (stipping all `Markdown` markup from the
        content). Defauts to `html`.
    strip_top_level_tags : bool
        Whether the top level tags should be stripped from the `Markdown` content.

    Returns
    -------
    : str
        Table of Contents of the converted document.
    : str
        `Markdown` converted to the requested format, using the provided extensions.
    """
    md = Markdown(extensions=extensions, output_format=output_format)  # type: ignore
    md.stripTopLevelTags = strip_top_level_tags  # type: ignore

    html = md.convert(mdwn)
    toc = md.toc

    return toc, html


def process_document(filepath: str) -> tuple[dict[str, str], str, str]:
    """Umbrella function to process fully an input file _completely_.

    Parameters
    ----------
    filepath : str
        Path to the `Markdown` file.

    Returns
    -------
    : dict[str, str]
        Metadata, extracted from the front matter or generated.
    : str
        Table of Contents of the converted document.
    : str
        `Markdown` content converted to HTML.
    : str
        Clean up `Markdown` content, ready to be indexed by
        [`lunr.js`](https://lunrjs.com/) (or its `Python` sibling,
        [`lunr.py`](https://lunr.readthedocs.io/)).
    """
    # check extension respective documentations for configuration
    extensions: list[Extension] = [
        AstdocsExtension(),
        DeleteSubExtension(),
        EmojiExtension(emoji_index=gemoji),
        FootnoteExtension(BACKLINK_TEXT=""),
        HighlightExtension(use_pygments=False),
        ImgExtension(),
        InsertExtension(parent_path=os.path.dirname(os.path.realpath(filepath))),
        InsertSupExtension(),
        MarkdownInHtmlExtension(),
        ScriptExtension(),
        SuperFencesCodeExtension(
            custom_fences=[
                {"name": "mermaid", "class": "mermaid", "format": fence_div_format},
                {"name": "naiad", "class": "naiad", "format": fence_div_format},
            ]
        ),
        TableExtension(),
        TocExtension(),
    ]

    # text to replace non-indexable content
    ellipsis: str = " [...] "

    # fetch markdown content and convert to html
    meta, mdwn = load_document(filepath)
    toc, html = convert_document(mdwn, extensions=extensions)

    # escape certain code blocks (otherwise mangled during minifying)
    for m in ("mermaid", "naiad"):
        html = re.sub(
            f'(<div class="{m}">.*?</div>)',
            (
                "<!-- htmlmin:ignore -->\n"
                "<!-- prettier-ignore -->\n"
                r"\1\n"
                "<!-- htmlmin:ignore -->"
            ),
            html,
            flags=re.DOTALL,
        )

    # clean markdown from markup and convert to plain text
    mdwn = clean_document(mdwn, ellipsis)
    _, text = convert_document(
        mdwn, extensions=extensions, output_format="text", strip_top_level_tags=False
    )

    # remove useless spacing and duplicated ellipsis
    # .strip() in case the placeholder contains spaces
    _ = len(text) + 1
    while _ > len(text):
        _ = len(text)
        cleaned_ellipsis = ellipsis.strip()
        text = text.replace(f"{cleaned_ellipsis} {cleaned_ellipsis}", cleaned_ellipsis)
        text = re.sub(r"\s+", " ", text)

    return meta, toc, html, text


def index_documents(texts: dict[str, str]) -> str:
    """Index all documents for [`lunr.js`](https://lunrjs.com/).

    Parameters
    ----------
    texts : dict[str, str]
        Path: plain text content pairs to be indexed by `Lunr`. Expects `%%%SECTION` and
        `%%%PARAGRAPH` markers to split the document in sections.

    Returns
    -------
    : str
        JSON content ready to be loaded by [`lunr.py`](https://lunr.readthedocs.io/).
    """
    documents: dict[str, str] = {}

    # add position to the metadata
    builder = get_default_builder()
    builder.metadata_whitelist.append("position")

    # split per section
    for filepath, text in texts.items():
        endpoint = re.sub("index.html$", "", filepath)

        for section in text.split("%%%SECTION"):

            if "%%%PARAGRAPH" in section:
                title, section = section.split("%%%PARAGRAPH")
                anchor = title.lower().replace(".", "").replace(" ", "-")  # github
                href = f'{endpoint}#{anchor}'
            else:
                href = endpoint

            section = section.strip()
            if len(section):
                documents[href] = section

    # convert to json
    return json.dumps(
        {
            "documents": documents,
            "indexed": lunr(
                ref="path",
                fields=["text"],
                documents=[{"path": p, "text": t} for p, t in documents.items()],
                builder=builder,
            ).serialize(),
        }
    )


# https://stackoverflow.com/a/54923798
# https://github.com/Python-Markdown/markdown/blob/master/markdown/core.py#L46
# function name follows the standard from the other converters
def to_text_string(
    element: xml.etree.ElementTree.Element, stream: io.StringIO = None
) -> str:
    """Serialize Markdown content into plain text."""
    if stream is None:
        stream = io.StringIO()

    if element.text:
        stream.write(element.text)

    for e in element:
        to_text_string(e, stream)

    if element.tail:
        stream.write(element.tail)

    return stream.getvalue()


# patching object
Markdown.output_formats["text"] = to_text_string  # type: ignore

if __name__ == "__main__":

    # keep track of the output and documents to be processed for lunr
    metas: dict[str, dict[str, str]] = {}
    htmls: dict[str, str] = {}
    texts: dict[str, str] = {}

    # flags
    parser = argparse.ArgumentParser(description="Render and index Markdown content.")
    parser.add_argument(
        "-p",
        "--prefix",
        default=".",
        help="Path prefix for the output (where generated content will be written).",
    )
    parser.add_argument(
        "-r",
        "--root",
        default="http://localhost:8000/",
        help="Root of the exposed content.",
    )
    parser.add_argument(
        "-t",
        "--template",
        default="template.html",
        help="Path to the HTML template to use during conversion.",
    )
    flags, files = parser.parse_known_args()

    # process the markdown file
    tmpl = load_template(flags.template)

    # for each argument...
    for filepath in files:

        # quick path clean up
        if filepath.startswith("./"):
            filepath = filepath.replace("./", "", 1)

        # path gymnastics
        dirname = "/".join(filepath.lstrip("./").split("/")[:-1])
        basename = filepath.split("/")[-1]
        output = re.sub(r"\.md$", ".html", f"{dirname}/{basename}".strip("/"))

        # process the markdown file
        meta, toc, html, text = process_document(filepath)
        html = render_template(flags.root, tmpl, meta, toc, html)

        # save content for later
        metas[output] = meta
        htmls[output] = html
        texts[output] = text

    # documents and pre-indexed content to be parsed by lunr
    index = index_documents(texts)

    # output each page
    for o, p in htmls.items():
        with open(f"{flags.prefix}/{o}", "w") as f:
            f.write(p)

    # output index
    with open(f"{flags.prefix}/lunr-index.json", "w") as f:
        f.write(index)
