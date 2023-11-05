**Templates for rendering `Markdown` into HTML.** For my opinionated usage.

# Rendering

## Server-side

Rendering done via [`Python-Markdown`](https://python-markdown.github.io/). Plenty
extensions to deal with the fancy stuff, see below. Styling code (`.css` files) are
processed through [`autoprefixer`](https://github.com/postcss/autoprefixer) to add
vendor prefxes.

Served files could be prettified via [Prettier](https://github.com/prettier/prettier),
but are currently minified using a mix of [cssnano](https://github.com/cssnano/cssnano),
[html-minifier](https://github.com/kangax/html-minifier) and
[terser](https://github.com/terser/terser).

### Extensions

* [`AstdocsExtension`](https://github.com/carnarez/markdown-astdocs/) to parse
  [`astdocs`](https://github.com/carnarez/astdocs/)-specific syntax.
* [`DeleteSubExtension`](https://facelessuser.github.io/pymdown-extensions/extensions/tilde/)
  to introduce crossed out and subscript text.
* [`EmojiExtension`](https://python-markdown.github.io/extensions/emoji/) to add support
  for [GitHub emojis](https://github.com/github/gemoji).
* [`FootnoteExtension`](https://python-markdown.github.io/extensions/footnotes/) to
  handle, well, footnotes.
* [`HighlightExtension`](https://facelessuser.github.io/pymdown-extensions/extensions/highlight/)
  to single out code blocks.
* [`ImgExtension`](https://github.com/carnarez/markdown-img/) for a [slightly] smarter
  image management via options embedded in the usual `![]()` marker.
* [`InsertExtension`](https://github.com/carnarez/markdown-insert/) to support addition
  of external content into the processed document via the `&[]()` marker.
* [`InsertSupExtension`](https://facelessuser.github.io/pymdown-extensions/extensions/caret/)
  to introduce underlined and superscript text.
* [`MarkdownInHtmlExtension`](https://python-markdown.github.io/extensions/md_in_html/)
  to parse and render Markdown located *within* HTML blocks.
* [`ScriptExtension`](https://github.com/carnarez/markdown-script) to include
  `JavaScript` content via the `%[]()` marker.
* [`SuperFencesCodeExtension`](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
  to enhance the processing of fenced blocks.
* [`TableExtension`](https://python-markdown.github.io/extensions/tables/) to render
  tables.
* [`TocExtension`](https://python-markdown.github.io/extensions/toc/) to generate the
  table of contents and anchor the titles.

### Front matter

Front matter options (in _valid_ [YAML v1.1 format](https://yaml.org/spec/1.1/)) are
extracted from any `index.md` file via regular expression and properly parsed using
[`PyYAML`](https://github.com/yaml/pyyaml). Supported [keys](https://ogp.me/) listed
below.

The whole front matter block (including `---` markers) is removed from the document
before processing it.

#### Metatags

* `author` for the `article:author` metatag;
* `description` for the `og:description` metatag;
* `image` for the `og:image` metatag (above 1200x650 pixels for high resolution screens);
* `date` for the `article:published_time` metatag (`YYYY/MM/DD` format);
* `tags` for the `article:tag` metatag (list of keywords);
* `title` for the `og:title` metatag (defaults to the name of the folder otherwise);
* `url` for the `og:url` metatag;

Aside from `title`, all metatags are left empty if absent from the front matter.

#### Extras

* `canonical` to provide the canonical link of the article (defaults to `url` if not
   provided).
* `link` to provide a link to the author's favourite website.
* `logo` to provide a top-bar logo.

## Client-side

Once generated, some extra rendering is done in the browser -*i.e.*, on the client- via
a couple `JavaScript` libraries:

* [`highlight.js`](https://highlightjs.org/) for syntax highlighting.
* [`KaTeX`](https://katex.org/) to render equations written in LaTeX.
* [`Mermaid`](https://mermaidjs.github.io/) to render diagrams and flowcharts.

# Deploy locally

Run `make serve` to get the HTTP server started at
[http://localhost:8000/](http://localhost:8000/) using ~~a niftily
[patched](https://blog.oddbit.com/post/2015-01-04-building-a-minimal-web-server-for-testing-kubernetes/)
[`thttpd`](https://acme.com/software/thttpd/) as a *very* lightweight solution for
local development and testing or~~ the tiny solution shipped with [BusyBox](https://www.busybox.net/),
[`httpd`](https://www.busybox.net/downloads/BusyBox.html#httpd), although still
slightly bigger than the `thttpd` solution previously used.
