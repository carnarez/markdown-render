"""Parse front matter and generate a list of articles."""

import os
import re
import sys
import typing

from yaml import Loader, load

page: str = ""

for arg in sys.argv[1:]:
    with open(arg) as f:
        text: str = f.read().strip()

    # extract front matter
    meta: dict[str, typing.Any] = {}
    rgxp: re.Pattern = re.compile(r"^---\n(.+?)\n---\n\n", flags=re.DOTALL)
    if text.startswith("---"):
        try:
            meta = load(re.match(rgxp, text).group(1), Loader=Loader)  # type: ignore
        except AttributeError:
            pass

    t = meta.get("title", arg.split("/")[-2].replace(".md", "").capitalize())
    u = meta["url"] = os.path.dirname(arg).lstrip(".")

    page += f"#### [{t}]({u})\n\n"

# output to stdout
sys.stdout.write(page)
