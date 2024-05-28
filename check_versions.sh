#!/bin/bash

function extract_version_from_releases {
  curl -L -o /dev/null -s -w %{url_effective} https://github.com/$1/releases/latest | awk -F'/' '{print$NF}' | sed 's/^v//g'
}

function extract_version_from_tags {
  curl -L -s https://github.com/olivernn/lunr.js/tags | grep -E -m 1 -o "/$1/releases/tag/v[0-9.]+" | awk -F'/' '{print$NF}' | sed 's/v//g'
}

grep cdnjs markdown_render/template.html | awk -F'/' '{print$6,$7}' | sort | uniq

echo

echo KaTeX $(extract_version_from_releases KaTeX/KaTeX)
echo highlight.js $(extract_version_from_releases highlightjs/highlight.js)
echo lunr.js $(extract_version_from_tags olivernn/lunr.js)
echo mermaid $(extract_version_from_releases mermaid-js/mermaid)
