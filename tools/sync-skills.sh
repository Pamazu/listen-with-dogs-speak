#!/bin/bash
# Refresh skills/ from the brain, where the skills are maintained. Run on J's Mac:
#   tools/sync-skills.sh
set -euo pipefail
BRAIN="${BRAIN_SKILLS:-$HOME/All/0_Global/skills}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for s in timed-video-prompts consistent-character-images; do
  rsync -a --delete \
    --exclude '/sources/higgsfield-timed-prompts/' \
    --exclude '.DS_Store' --exclude '__pycache__/' \
    "$BRAIN/$s/" "$ROOT/skills/$s/"
done
# The original timed-prompts skill has no known licence: it must never be published here.
if [ -e "$ROOT/skills/timed-video-prompts/sources/higgsfield-timed-prompts" ]; then
  echo "refusing: the unlicensed original is in skills/; remove it before committing" >&2
  exit 1
fi
echo "skills/ refreshed from $BRAIN"
