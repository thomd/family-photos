#!/usr/bin/env bash

[ -z "$1" ] && echo >&2 "folder required!" && exit 1
cd "$1" || exit 1

N=$(find . -type f | wc -l)

yesno() {
  read -r -p "$1 [y/N] " response
  [[ $response == "y" || $response == "Y" ]] || exit 1
}
yesno "distribute $(tput setaf 2)${N// /}$(tput sgr 0) images in $(tput setaf 2)$(pwd)$(tput sgr 0) ?"

COUNT=0
while IFS= read -r -d '' F; do
  D=$(exiftool "$F" | grep "Create Date" | head -n 1 | awk '{print $4}' | tr ':' '-')
  DD=$(echo "$D" | cut -c 1-4)
  COUNT=$((COUNT+1))
  FF=$(basename "$F" | tr -s ' ' '-')
  mkdir -p "$DD/$D";
  mv "$F" "$DD/$D/$FF";
  echo "$(tput setaf 2)[$COUNT/${N// /}]$(tput sgr 0) $(pwd)/$DD/$D/$FF"
done < <(find . -maxdepth 1 -type f -iname "*.jpg" -print0)
