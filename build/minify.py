"""Minify the HTML content while protecting specific code blocks."""

import re
import sys
import typing

import minify_html


def extract(
    s: str,
    patterns: typing.List[str],
    repl_prefix: str = "%%%REPL",
    repl_suffix: str = "%%%"
) -> typing.Tuple[str, typing.Dict[str, str]]:
    """Extract protected code blocks and replace them by a pattern.

    Parameters
    ----------
    s : str
        The string to process.
    patterns : typing.List[str]
        The list of patterns used to identify and extract the content to protect. An
        example is `<div class="mermaid">(.*?)</div>` to protect the Mermaid code
        blocks otherwise minified (yielding ).
    repl_prefix : str
        Suffix of the replacing pattern. Defaults to `%%%REPL`. Note an iterator will
        be concatenated to the suffix to make it unique.
    repl_suffix : str
        Prefix of the replacing pattern. Defaults to `%%%`.

    Returns
    -------
    : typing.Tuple[str, typing.Dict[str, str]]
        String with protected code blocks replaced by patterns, and a dictionary
        listing the patterns: original content pairs.
    """
    extracted: typing.Dict[str, str] = {}

    for p in patterns:
        for i, m in enumerate(re.finditer(p, s, flags=re.DOTALL)):
            repl = f"{repl_prefix}{i}{repl_suffix}"
            extracted[repl] = m.group(1)
            s = s.replace(m.group(1), repl)

    return s, extracted


def minify(s: str) -> str:
    """Minify the HTML content.

    This is kept as a function to keep track of the options passed to the
    `minify_html.minify` method. Those parameters were extracted from the `Rust` code
    available
    [there](https://github.com/wilsonzlin/minify-html/blob/master/python/src/lib.template.rs).

    Parameters
    ----------
    s : str
        Content to process.

    Returns
    -------
    : str
        Minified content.

    Notes
    -----
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
    """
    s = minify_html.minify(
        s,
        minify_css=True,
        minify_js=True,
        do_not_minify_doctype=True,
        ensure_spec_compliant_unquoted_attribute_values=True,
        keep_closing_tags=False,
        keep_comments=False,
        keep_html_and_head_opening_tags=True,
        keep_spaces_between_attributes=True,
        remove_bangs=True,
        remove_processing_instructions=True,
    )

    s = s.replace("&LT", "<")

    return s


def replace(s: str, repl_dict: typing.Dict[str, str]):
    """Alternate replace function allowing for dictionaries.

    Parameters
    ----------
    s : str
        The string to process.
    repl_dict : typing.Dict[str, str]
        Dictionary of old: new pairs.

    Returns
    -------
    : str
        Processed string.
    """
    for old, new in repl_dict.items():
        s = s.replace(old, new)

    return s


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        c, e = extract(
            f.read(),
            [
                # protect the mermaid code blocks (not bounded by <pre>...</pre> tags)
                # note that the regular expression needs to be non-greedy (?)
                '<div class="mermaid">(.*?)</div>',
            ],
        )
        c = minify(c)
        c = replace(c, e)  # alternate replace
        print(c)
