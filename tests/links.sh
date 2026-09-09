#!/bin/bash
# P304 amendment. EVERY href on the trial pages is loaded from the PUBLIC
# INTERNET before any deploy. Written because the demo button 404'd in the
# Director's hand at the event: the page had been verified and the link
# behind it had not. A page is not verified until every destination is.
#
# Run: bash tests/links.sh
set -u
BASE="https://abed92009-cell.github.io/pages"
PAGES="try/ try/w/"
ASSETS="try/detter-try.png try/detter-try.svg try/detter-try-card.pdf
        try/mirrormirror/manifest.webmanifest try/mirrormirror/icon-192.png
        try/mirrormirror/icon-512.png"
fail=0
check () {  # url, label
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 25 -L "$1")
  printf '  %-72s %s\n' "$1" "$code"
  [ "$code" = "200" ] || { fail=$((fail+1)); }
}
echo "PAGES"
for p in $PAGES; do check "$BASE/$p"; done
echo "EVERY href ON EVERY PAGE, resolved the way a browser resolves it"
for p in $PAGES; do
  html=$(curl -s --max-time 25 "$BASE/$p")
  for h in $(printf '%s' "$html" | grep -oE 'href="[^"]*"' | sed 's/href="//;s/"//' | grep -v '^#'); do
    case "$h" in
      http*)  url="$h" ;;
      /*)     url="https://abed92009-cell.github.io$h" ;;
      *)      url="$BASE/$p$h" ;;   # relative: resolved against THIS page
    esac
    check "$url"
  done
done
echo "ASSETS"
for a in $ASSETS; do check "$BASE/$a"; done
echo
if [ "$fail" -gt 0 ]; then echo "FAIL: $fail destination(s) did not return 200"; exit 1; fi
echo "PASS: every destination returns 200"
