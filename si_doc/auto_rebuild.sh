#/bin/bash
inotifywait -e close_write,moved_to,create -m .  |
while read -r directory events filename; do
  if [ "${filename##*.}" = "tex" ]; then
    echo "${filename##*.}"
    make
  fi
done

