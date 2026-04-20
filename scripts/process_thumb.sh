#!/bin/bash
# Process a project thumbnail: resize to max 600px, convert to JPG.
#
# Usage:
#   bash scripts/process_thumb.sh <source.png> <project-name>
#
# Example:
#   bash scripts/process_thumb.sh ~/Downloads/projects/large-models/thumbnail.png large-models
#
# Output goes to img/projects/<project-name>/thumb.jpg

set -e

SRC="$1"
PROJECT="$2"

if [[ -z "$SRC" || -z "$PROJECT" ]]; then
  echo "Usage: $0 <source-image> <project-name>"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DST="$REPO_ROOT/img/projects/$PROJECT/thumb.jpg"
TMP=$(mktemp /tmp/thumb_XXXX.png)

# Resize to max 600px on longest side
sips -Z 600 "$SRC" --out "$TMP" 2>/dev/null

# Convert to JPG at quality 80
sips -s format jpeg -s formatOptions 80 "$TMP" --out "$DST" 2>/dev/null

rm -f "$TMP"
echo "✓ $DST  ($(stat -f%z "$DST") bytes)"
