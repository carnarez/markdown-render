"""Template script to render Markdown to HTML. Fanciness included."""

from markdown import markdown
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

tpl = """
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="style.css">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script
    defer
    src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"
    onload="hljs.highlightAll();"
  ></script>
  <script
    defer
    src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"
    onload="mermaid.initialize();"
  ></script>
  <script
    defer
    src="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js"
  ></script>
  <script
    defer
    src="https://cdn.jsdelivr.net/npm/katex/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(
      document.body,
      {delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false},
      ]}
    );"
  ></script>
  <script>
    function setTheme(name) {
      localStorage.setItem("theme", name);
      document.documentElement.className = name;
    }
    function toggleTheme() {
      if (localStorage.getItem("theme") === "light") {
        setTheme("dark_dimmed");
      } else {
        setTheme("light");
      }
    }
    if (
      localStorage.getItem("theme") === "dark_dimmed" ||
      (
        !("theme" in localStorage) &&
        window.matchMedia("(prefers-color-scheme: dark)").matches
      )
    ) {
      setTheme("dark_dimmed");
    } else {
      setTheme("light");
    }
  </script>
  <title>Markdown rendering test</title>
</head>
<body>

HTML

<a onclick="toggleTheme();">theme</a>
</body>
</html>
"""

# check extension respective documentations for configuration
exts = [
    AstdocsExtension(),
    DeleteSubExtension(),
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
print(
    tpl.replace(
        "HTML", markdown(f'[TOC]\n\n{open("markdown.md").read()}', extensions=exts)
    )
)
