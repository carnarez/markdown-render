# Module `minify`

Minify the HTML content while protecting specific code blocks.

**Functions:**

* [`extract()`](#minifyextract): Extract protected code blocks and replace them by a pattern.
* [`minify()`](#minifyminify): Minify the HTML content.
* [`replace()`](#minifyreplace): Alternate replace function allowing for dictionaries.

## Functions

### `minify.extract`

```python
extract(
    s: str, 
    patterns: typing.List[str], 
    repl_prefix: str, 
    repl_suffix: str,
) -> typing.Tuple[str, typing.Dict[str, str]]:
```

Extract protected code blocks and replace them by a pattern.

**Parameters:**

* `s` [`str`]: The string to process.
* `patterns` [`typing.List[str]`]: The list of patterns used to identify and extract the content to protect. An
    example is `<div class="mermaid">(.*?)</div>` to protect the Mermaid code
    blocks otherwise minified (yielding ).
* `repl_prefix` [`str`]: Suffix of the replacing pattern. Defaults to `%%%REPL`. Note an iterator will
    be concatenated to the suffix to make it unique.
* `repl_suffix` [`str`]: Prefix of the replacing pattern. Defaults to `%%%`.

**Returns:**

* [`typing.Tuple[str, typing.Dict[str, str]]`]: String with protected code blocks replaced by patterns, and a dictionary
    listing the patterns: original content pairs.

### `minify.minify`

```python
minify(s: str) -> str:
```

Minify the HTML content.

This is kept as a function to keep track of the options passed to the
`minify_html.minify` method. Those parameters were extracted from the `Rust` code
available
[there](https://github.com/wilsonzlin/minify-html/blob/master/python/src/lib.template.rs).

**Parameters:**

* `s` [`str`]: Content to process.

**Returns:**

* [`str`]: Minified content.

**Notes:**

* [`minify-html`](https://github.com/wilsonzlin/minify-html) configuration is as
  follows:
    * `do_not_minify_doctype` is set to `True`;
    * `ensure_spec_compliant_unquoted_attribute_values` is set to `True`;
    * `keep_closing_tags` is set to `False`;
    * `keep_comments` is set to `False`;
    * `keep_html_and_head_opening_tags` is set to `True`;
    * `keep_spaces_between_attributes` is set to `True;
    * `remove_bangs` is set to `True`;
    * `remove_processing_instructions` is set to `True`.
* Some weird choices from `minify-html` are also reverted; notably the `&LT` are
  substituted back to `<`.

### `minify.replace`

```python
replace(s: str, repl_dict: typing.Dict[str, str]):
```

Alternate replace function allowing for dictionaries.

**Parameters:**

* `s` [`str`]: The string to process.
* `repl_dict` [`typing.Dict[str, str]`]: Dictionary of old: new pairs.

**Returns:**

* [`str`]: Processed string.

# Module `render`

Template script to render Markdown to HTML. Fanciness included.
