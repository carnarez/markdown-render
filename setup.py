"""Make this little DIY installable (via `pip install git+https://...`)."""

import setuptools

setuptools.setup(
    author="carnarez",
    description=("Opinionated way to render `Markdown` into web pages."),
    entry_points={"console_scripts": ["render-markdown=markdown_render.render:cli"]},
    install_requires=["markdown", "pyyaml"],
    name="markdown-render",
    packages=["markdown_render"],
    package_data={"markdown_render": ["py.typed", "template.html"]},
    url="https://github.com/carnarez/markdown-render",
    version="0.0.1",
)
