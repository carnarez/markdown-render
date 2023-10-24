# Module `render`

Template script to render `Markdown` to HTML and index the content for Lunr.

**Arguments**

- `meta`: Extra metadata attributes for the frontmatter, separated by pipes (`|`).
  Defaults to an empty string.
- `prefix`: Prefix to the output path. Defaults to `.` (current directory).
- `root`: Root of the exposed content. Defaults to `http://localhost:8000/`.
- `template`: Path to the HTML template. Defaults to `template.html`.
- `toc`: Path to the overall table of contents (in Markdown format). Defaults to
  `toc.md`.

**Examples**

```shell
$ python render.py *.md
$ python render.py --meta="splash=splash.png|description=This is a description." *.md
$ python render.py --prefix=/var/www *.md
$ python render.py --template=template.html *.md
```

**Functions**

- [`load_template()`](#renderload_template): Load the `Jinja2` template.
- [`render_template()`](#renderrender_template): Render the `Jinja2` template after
  checking for presence of specific content.
- [`load_document()`](#renderload_document): Fetch the `Markdown` content and process
  present front matter.
- [`clean_document()`](#renderclean_document): Remove `Markdown` syntax from raw
  content.
- [`convert_document()`](#renderconvert_document): Convert the `Markdown` content to
  supported formats.
- [`process_document()`](#renderprocess_document): Umbrella function to process fully an
  input file _completely_.
- [`process_toc()`](#renderprocess_toc): Render the overall table of contents.
- [`merge_digests()`](#rendermerge_digests): Insert the document table of contents into
  the ovrall table of contents.
- [`index_documents()`](#renderindex_documents): Index all documents for
  [`lunr.js`](https://lunrjs.com/).
- [`to_text_string()`](#renderto_text_string): Serialize Markdown content into plain
  text.

## Functions

### `render.load_template`

```python
load_template(filepath: str = "./template.html") -> Template:
```

Load the `Jinja2` template.

**Parameters**

- `filepath` \[`str`\]: Path to the `Jinja2` HTML template. Defaults to
  `./template.html`.

**Returns**

- \[`jinja2.Template`\]: `Jinja2` template ready to be used.

### `render.render_template`

```python
render_template(
    root: str,
    tmpl: Template,
    meta: dict[str, str],
    toc: str,
    html: str,
) -> str:
```

Render the `Jinja2` template after checking for presence of specific content.

**Parameters**

- `root` \[`str`\]: Root of the served content.
- `tmpl` \[`jinja2.Template`\]: `Jinja2` template ready to be used.
- `meta` \[`dict[str, str]`\]: Metadata, extracted from the front matter or generated.
- `toc` \[`str`\]: Table of contents of the converted document.
- `html` \[`str`\]: Generated HTML content.

**Returns**

- \[`str`\]: Rendered HTML content.

**Note**

The current check for equations easily returns false positives.

### `render.load_document`

```python
load_document(filepath: str) -> tuple[dict[str, str], str]:
```

Fetch the `Markdown` content and process present front matter.

**Parameters**

- `filepath` \[`str`\]: Path to the `Markdown` file.

**Returns**

- \[`dict[str, str]`\]: Metadata, extracted from the front matter or generated.
- \[`str`\]: Raw `Markdown` content.

### `render.clean_document`

```python
clean_document(mdwn: str, ellipsis: str = " [...] ") -> str:
```

Remove `Markdown` syntax from raw content.

**Parameters**

- `mdwn` \[`str`\]: Raw `Markdown` content to process.
- `ellipsis` \[`str`\]: Text to replace non-indexable content. Defaults to `[...]`
  (including the leading/trailing space).

**Returns**

- \[`str`\]: Cleaned up content.

**Note**

Replace the following string by the provided ellipsis:

- Table of contents markers `[TOC]`.
- All footnote markers.
- All code blocks.
- [`astdocs`](https://github.com/carnarez/astdocs) `%%%SOURCE`, `%%%START` and
  `%%%END`markers.
- All equations (might cause some false positive).
- All special syntax: `![]()`, `%[]()`, `&[]()`.
- All HTML tags.

### `render.convert_document`

```python
convert_document(
    mdwn: str,
    extensions: list[Extension],
    output_format: str = "html",
    strip_top_level_tags: bool = True,
) -> tuple[str, str]:
```

Convert the `Markdown` content to supported formats.

**Parameters**

- `mdwn` \[`str`\]: Raw `Markdown` content to process.
- `extensions` \[`list[markdown.extensions.Extension]`\]: List of
  [extensions](https://python-markdown.github.io/extensions/) to apply during the
  conversion.
- `output_format` \[`str`\]: Output format after conversion. Note the the patched
  `markdown.Markdown` object supports the `text` conversion (stipping all `Markdown`
  markup from the content). Defauts to `html`.
- `strip_top_level_tags` \[`bool`\]: Whether the top level tags should be stripped from
  the `Markdown` content.

**Returns**

- \[`str`\]: Table of contents of the converted document.
- \[`str`\]: `Markdown` converted to the requested format, using the provided
  extensions.

### `render.process_document`

```python
process_document(filepath: str) -> tuple[dict[str, str], str, str]:
```

Umbrella function to process fully an input file _completely_.

**Parameters**

- `filepath` \[`str`\]: Path to the `Markdown` file.

**Returns**

- \[`dict[str, str]`\]: Metadata, extracted from the front matter or generated.
- \[`str`\]: Table of contents of the converted document.
- \[`str`\]: `Markdown` content converted to HTML.
- \[`str`\]: Clean up `Markdown` content, ready to be indexed by
  [`lunr.js`](https://lunrjs.com/) (or its `Python` sibling,
  [`lunr.py`](https://lunr.readthedocs.io/)).

### `render.process_toc`

```python
process_toc(filepath: str) -> str:
```

Render the overall table of contents.

**Parameters**

- `filepath` \[`str`\]: Path to the `Markdown` file.

**Returns**

- \[`str`\]: `Markdown` content converted to HTML.

### `render.merge_digests`

```python
merge_digests(endpoint: str, global_toc: str, page_toc: str):
```

Insert the document table of contents into the ovrall table of contents.

**Parameters**

- `endpoint` \[`str`\]: Internal URL to the served content.
- `global_toc` \[`str`\]: Overall table of contents.
- `page_toc` \[`str`\]: Table of contents of the converted document.

**Returns**

- \[`str`\]: HTML table of contents.

### `render.index_documents`

```python
index_documents(texts: dict[str, str]) -> str:
```

Index all documents for [`lunr.js`](https://lunrjs.com/).

**Parameters**

- `texts` \[`dict[str, str]`\]: Path: plain text content pairs to be indexed by `Lunr`.
  Expects `%%%SECTION` and `%%%PARAGRAPH` markers to split the document in sections.

**Returns**

- \[`str`\]: JSON content ready to be loaded by
  [`lunr.py`](https://lunr.readthedocs.io/).

### `render.to_text_string`

```python
to_text_string(
    element: xml.etree.ElementTree.Element,
    stream: io.StringIO = None,
) -> str:
```

Serialize Markdown content into plain text.
