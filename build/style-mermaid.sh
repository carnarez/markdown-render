src=https://raw.githubusercontent.com/mermaid-js/mermaid/develop/src/themes/theme-base.js

echo "// all variables extracted and modified from the source at
// $src

function mermaidInitialize() {
  let style = getComputedStyle(document.body);" > mermaid.js

wget -O - -qq $src \
    | grep -E -e "    this.[A-Za-z0-9]+ =" -e "\/\*" \
    | grep -v tstates \
    | sed -r '2d;s/^    //g;s/this.//g;s/[A-Za-z0-9]+ \|\| //g;s#^/#\n  //#g;s/^([a-z])/  let \1/g;s/\*//g;s#/$#\n#g;s/# //g;s#// .*$#\L&#g;s/ variables//g;s#; // .*$##g' \
    >> mermaid.js

echo '
  mermaid.initialize({
    "theme": "base",
    "themeVariables": {' >> mermaid.js

grep 'let' mermaid.js \
    | awk '{printf"      \"%s\": %s,\n",$2,$2}' \
    | grep -v style \
    | sort \
    | uniq \
    >> mermaid.js

echo '    }
  });
}' >> mermaid.js

cat mermaid.js
