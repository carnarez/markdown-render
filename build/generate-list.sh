find /tmp/prose -name index.html | while read f; do
  (
  if [ $(head -1 $f | tr -d " ") == '---' ]; then
    export $(sed -n '1,/---/p' prose/tests/index.md | sed '1d;$d;s/: /=/g')
    if [ -z $title ]; then
      echo -e "# [$title]($url)\n"
      echo -e "![]($image)\n"
      echo -e "by [$author]($link) on $published_date\n"
      echo -e "$description\n"
      echo -e "$tags"
    fi
  fi
  )
done
