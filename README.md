**Templates for rendering and styling Markdown-generated HTML.** For my opinionated
usage, hate if you will.

Rendering done via [`Python-Markdown`](https://python-markdown.github.io/). Plenty
extensions to deal with the fancy stuff:

* [`AstdocsExtension`](https://github.com/carnarez/markdown-astdocs/) to parse
  [`astdocs`](https://github.com/carnarez/astdocs/)-specific syntax.
* [`DeleteSubExtension`](https://facelessuser.github.io/pymdown-extensions/extensions/tilde/)
  to introduce crossed out and subscript text.
* [`FootnoteExtension`](https://python-markdown.github.io/extensions/footnotes/) to
  handle, well, footnotes.
* [`HighlightExtension`](https://facelessuser.github.io/pymdown-extensions/extensions/highlight/)
  to single out code blocks.
* [`ImgExtension`](https://github.com/carnarez/markdown-img/) for a [slightly] smarter
  image management.
* [`InsertExtension`](https://github.com/carnarez/markdown-insert/) to support addition
  of external content into the processed document.
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

Once generated, some extra rendering is done in the browser -*i.e.*, on the client- via
a couple `JavaScript` libraries donwloaded from [cdnjs.com](https://cdnjs.com/):

* [`highlight.js`](https://highlightjs.org/) for syntax highlighting.
* [`KaTeX`](https://katex.org/) to render equations written in LaTeX.
* [`Mermaid`](https://mermaidjs.github.io/) to render diagrams and flowcharts.

Basic styling (and syntax highlighting) forked from GitHub colour scheme; see
[`style-highlight.sh`](build/style-highlight.sh). Crude light/dark (dimmed) toggler included.
But the `Mermaid` [stylesheet](static/style-mermaid.css) will forever be in progress...

Run `make serve` to get the HTTP server started at
[http://localhost:8000/](http://localhost:8000/), using
* ~~a niftily
  [patched](https://blog.oddbit.com/post/2015-01-04-building-a-minimal-web-server-for-testing-kubernetes/)
  [`thttpd`](https://acme.com/software/thttpd/) as a *very* lightweight solution for
  local development and testing.~~
* the tiny solution shipped with [BusyBox](https://www.busybox.net/),
  [`httpd`](https://www.busybox.net/downloads/BusyBox.html#httpd), although still
  slightly bigger than the `thttpd` solution above (convince yourself by changing the
  source `Dockerfile`).
